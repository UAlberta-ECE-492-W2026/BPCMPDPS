from __future__ import annotations

import pandas as pd

from Model import DemandPrice
from .predictions import predict1215hrs
from forecasting.services import get_weather_forecast_by_horizon


def get_recent_price_data():
    df = pd.read_csv("Pricemodel/data/weather.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")
    df = df[["timestamp", "Price"]]
    return df.tail(240)

def get_weather_from_test_data(now: pd.Timestamp):
    df = pd.read_csv("Pricemodel/data/weather.csv")

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")

    results = {}

    for horizon in range(12, 16):
        target_time = now + pd.Timedelta(hours=horizon)

        row = df[df["timestamp"] == target_time]

        if row.empty:
            row = df.iloc[(df["timestamp"] - target_time).abs().argsort()[:1]]

        results[horizon] = {
            "temperature_c": float(row["temperature_c"].values[0]),
            "wind_speed_kph": float(row["wind_speed_kph"].values[0]),
        }
    return results


def save_Price(prices: list[dict]) -> list[DemandPrice]:
    saved = []
    for item in prices:
        obj, _ = DemandPrice.objects.update_or_create(
            prediction_time=item["prediction_time"],
            target_time=item["target_time"],
            horizon_steps=item["horizon_steps"],
            defaults={
                "predicted_Price": item["predicted_Price"],
                "model_vrs": item["model_vrs"],
            },
        )
        saved.append(obj)
    return saved


def run_get_Price() -> list[DemandPrice]:
    recent_price = get_recent_price_data()
    now =recent_price["timestamp"].iloc[-1]
    weather_by_horizon = get_weather_from_test_data(now)
    price = predict1215hrs(
        recent_price=recent_price,
        weather_by_horizon=weather_by_horizon,
    )
    return save_Price(price)