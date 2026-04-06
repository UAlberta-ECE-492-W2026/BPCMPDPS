from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd

from django.conf import settings
from django.utils import timezone

from .featurecreation import (
    FEATURE_COLUMNS,
    add_lag_features,
    add_rolling_features,
    add_time_features,
)
from forecasting.feature_engineering import add_weather_features



def load_model(horizon_steps: int = 12):
    model_path = Path(settings.BASE_DIR) / "Pricemodel" / "Versions" / f"price_h{horizon_steps}.joblib"
    if not model_path.exists():
        return None
    return joblib.load(model_path)

def build_latest_feature_row( recent_df: pd.DataFrame,Price_timestamp, Price_temperature_c: float = 0.0, Price_wind_speed_kph: float = 0.0,) -> pd.DataFrame:
    """
    Build one feature row using the most recent demand history plus target-time weather.
    recent_df must contain:
        timestamp, Price
    """
    df = recent_df.copy().sort_values("timestamp").reset_index(drop=True)

    df = add_lag_features(df, target_col="Price")
    df = add_rolling_features(df, target_col="Price")

    latest = df.iloc[[-1]].copy()
    latest["timestamp"] = pd.to_datetime([Price_timestamp])
    latest["temperature_c"] = Price_temperature_c
    latest["wind_speed_kph"] = Price_wind_speed_kph

    latest = add_time_features(latest, timestamp_col="timestamp")
    latest = add_weather_features(latest)

    return latest[FEATURE_COLUMNS]

def predict_single_horizon(recent_df: pd.DataFrame,horizon_steps: int, Price_timestamp, Price_temperature_c: float = 0.0, Price_wind_speed_kph: float = 0.0,) -> float:
    model = load_model(horizon_steps=horizon_steps)

    # fallback if model is not trained yet
    if model is None:
        return float(recent_df["Price"].iloc[-1])

    X = build_latest_feature_row(
        recent_df=recent_df,
        Price_timestamp=Price_timestamp,
        Price_temperature_c=Price_temperature_c,
        Price_wind_speed_kph=Price_wind_speed_kph,
    )
    pred = model.predict(X)[0]
    return float(pred)


def predict1215hrs(recent_df: pd.DataFrame, weather_by_horizon: dict[int, dict] | None = None,) -> list[dict]:
    """
    Returns predictions for horizons 12..15 (hours ahead).
    weather_by_horizon format:
    {
        12: {"temperature_c": 2.5, "wind_speed_kph": 12.0},
        ...
    }
    """
    if weather_by_horizon is None:
        weather_by_horizon = {}
    now = pd.to_datetime(recent_df["timestamp"].iloc[-1])
    results = []

    for horizon in range(12, 16):
        target_time = now + timezone.timedelta(hours=horizon)
        weather = weather_by_horizon.get(horizon, {})
        pred = predict_single_horizon(
            recent_df=recent_df,
            horizon_steps=horizon,
            Price_timestamp=target_time,
            Price_temperature_c=float(weather.get("temperature_c", 0.0)),
            Price_wind_speed_kph=float(weather.get("wind_speed_kph", 0.0)),
        )
        results.append(
            {
                "prediction_made_at": now,
                "target_time": target_time,
                "horizon_steps": horizon,
                "Price": pred,
                "model_version": f"price_h{horizon}",
            }
        )
    return results