from __future__ import annotations

from pathlib import Path

import pandas as pd
from django.conf import settings

from .Model import DemandPrice
from .predictions import predict1215hrs


def get_recent_price_data():
    csv_path = Path(settings.BASE_DIR) / "Pricemodel" / "data" / "Price_weather_testing.csv"
    df = pd.read_csv(csv_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")
    df = df[["timestamp", "Price"]]
    return df.tail(240)

def get_weather_from_test_data(now: pd.Timestamp):
    csv_path = Path(settings.BASE_DIR) / "Pricemodel" / "data" / "Price_weather_testing.csv"
    df = pd.read_csv(csv_path)

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
    """Maps the keys returned by predict1215hrs to the DemandPrice model fields."""
    saved = []
    for item in prices:
        obj, _ = DemandPrice.objects.update_or_create(
            prediction_time=item["prediction_made_at"],
            target_time=item["target_time"],
            horizon_steps=item["horizon_steps"],
            defaults={
                "predicted_Price": item["Price"],
                "model_vrs": item["model_version"],
            },
        )
        saved.append(obj)
    return saved


def run_get_Price() -> list[DemandPrice]:
    recent_price = get_recent_price_data()
    now = recent_price["timestamp"].iloc[-1]
    weather_by_horizon = get_weather_from_test_data(now)
    prices = predict1215hrs(
        recent_df=recent_price,
        weather_by_horizon=weather_by_horizon,
    )
    return save_Price(prices)