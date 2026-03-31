from __future__ import annotations

import pandas as pd
from django.utils import timezone

from .models import DemandForecast
from .predict import predict_12_to_15_hour_window
import requests

def get_recent_meter_data():
    df = pd.read_csv("forecasting/data/demand_weather_testing.csv")

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")

    df = df[["timestamp", "demand_kw"]]

    # last ~10 days (needed for lag features)
    return df.tail(240)


def get_weather_forecast_by_horizon(now):
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": 53.54087514959737,
        "longitude": -113.49119564477701,
        "hourly": "temperature_2m,wind_speed_10m",
        "forecast_days": 1,
    }

    response = requests.get(url, params=params)
    data = response.json()

    times = pd.to_datetime(data["hourly"]["time"])
    temps = data["hourly"]["temperature_2m"]
    winds = data["hourly"]["wind_speed_10m"]

    weather_df = pd.DataFrame({
        "timestamp": times,
        "temperature_c": temps,
        "wind_speed_kph": winds
    })

    results = {}

    for horizon in range(12, 16):
        target_time = now + pd.Timedelta(hours=horizon)

        row = weather_df.iloc[(weather_df["timestamp"] - target_time).abs().argsort()[:1]]

        results[horizon] = {
            "temperature_c": float(row["temperature_c"].values[0]),
            "wind_speed_kph": float(row["wind_speed_kph"].values[0]),
        }

    return results


def get_weather_from_test_data(now: pd.Timestamp):
    df = pd.read_csv("forecasting/data/demand_weather_testing.csv")

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")

    results = {}

    for horizon in range(12, 16):
        target_time = now + pd.Timedelta(hours=horizon)

        row = df[df["timestamp"] == target_time]

        if row.empty:
            # DST or missing timestamp → find closest match
            row = df.iloc[(df["timestamp"] - target_time).abs().argsort()[:1]]

        results[horizon] = {
            "temperature_c": float(row["temperature_c"].values[0]),
            "wind_speed_kph": float(row["wind_speed_kph"].values[0]),
        }

    return results


def save_forecasts(forecasts: list[dict]) -> list[DemandForecast]:
    saved = []
    for item in forecasts:
        obj, _ = DemandForecast.objects.update_or_create(
            prediction_made_at=item["prediction_made_at"],
            target_time=item["target_time"],
            horizon_steps=item["horizon_steps"],
            defaults={
                "predicted_demand_kw": item["predicted_demand_kw"],
                "model_version": item["model_version"],
            },
        )
        saved.append(obj)
    return saved


def run_demand_forecast() -> list[DemandForecast]:
    recent_df = get_recent_meter_data()
    now = recent_df["timestamp"].iloc[-1]
    # For real forecasts, we would get actual weather forecasts here instead of test data
    # weather_by_horizon = get_weather_forecast_by_horizon(now)

    # Using test data for consistent results and easier debugging
    weather_by_horizon = get_weather_from_test_data(now)
    forecasts = predict_12_to_15_hour_window(
        recent_df=recent_df,
        weather_by_horizon=weather_by_horizon,
    )
    return save_forecasts(forecasts)