from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd

from django.conf import settings
from django.utils import timezone

from .feature_engineering import (
    FEATURE_COLUMNS,
    add_lag_features,
    add_rolling_features,
    add_time_features,
    add_weather_features,
)


def load_model(horizon_steps: int = 12):
    model_path = Path(settings.BASE_DIR) / "forecasting" / "artifacts" / f"demand_model_h{horizon_steps}.joblib"
    if not model_path.exists():
        return None
    return joblib.load(model_path)


def build_latest_feature_row(
    recent_df: pd.DataFrame,
    forecast_timestamp,
    forecast_temperature_c: float = 0.0,
    forecast_wind_speed_kph: float = 0.0,
) -> pd.DataFrame:
    """
    Build one feature row using the most recent demand history plus target-time weather.
    recent_df must contain:
        timestamp, demand_kw
    """
    df = recent_df.copy().sort_values("timestamp").reset_index(drop=True)

    df = add_lag_features(df, target_col="demand_kw")
    df = add_rolling_features(df, target_col="demand_kw")

    latest = df.iloc[[-1]].copy()
    latest["timestamp"] = pd.to_datetime([forecast_timestamp])
    latest["temperature_c"] = forecast_temperature_c
    latest["wind_speed_kph"] = forecast_wind_speed_kph

    latest = add_time_features(latest, timestamp_col="timestamp")
    latest = add_weather_features(latest)

    return latest[FEATURE_COLUMNS]


def predict_single_horizon(
    recent_df: pd.DataFrame,
    horizon_steps: int,
    forecast_timestamp,
    forecast_temperature_c: float = 0.0,
    forecast_wind_speed_kph: float = 0.0,
) -> float:
    model = load_model(horizon_steps=horizon_steps)

    # fallback if model is not trained yet
    if model is None:
        return float(recent_df["demand_kw"].iloc[-1])

    X = build_latest_feature_row(
        recent_df=recent_df,
        forecast_timestamp=forecast_timestamp,
        forecast_temperature_c=forecast_temperature_c,
        forecast_wind_speed_kph=forecast_wind_speed_kph,
    )
    pred = model.predict(X)[0]
    return float(pred)


def predict_12_to_15_hour_window(
    recent_df: pd.DataFrame,
    weather_by_horizon: dict[int, dict] | None = None,
) -> list[dict]:
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

    # REAL-TIME MODE (future use)
    now = timezone.now()

    # TESTING MODE (2025 simulation)
    # now = pd.to_datetime(recent_df["timestamp"].iloc[-1])
    results = []

    for horizon in range(12, 16):
        target_time = now + timezone.timedelta(hours=horizon)
        weather = weather_by_horizon.get(horizon, {})
        pred = predict_single_horizon(
            recent_df=recent_df,
            horizon_steps=horizon,
            forecast_timestamp=target_time,
            forecast_temperature_c=float(weather.get("temperature_c", 0.0)),
            forecast_wind_speed_kph=float(weather.get("wind_speed_kph", 0.0)),
        )
        results.append(
            {
                "prediction_made_at": now,
                "target_time": target_time,
                "horizon_steps": horizon,
                "predicted_demand_kw": pred,
                "model_version": f"demand_h{horizon}",
            }
        )

    return results