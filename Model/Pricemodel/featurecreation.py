from __future__ import annotations

import pandas as pd
from forecasting.feature_engineering import add_time_features


def add_lag_features(df: pd.DataFrame, target_col: str = "Price", lags: list[int] | None = None,) -> pd.DataFrame:
    df = df.copy()
    if lags is None:
        lags = [1, 3, 6, 12, 24, 48, 168]

    for lag in lags:
        df[f"{target_col}_lag_{lag}"] = df[target_col].shift(lag)

    return df


def add_rolling_features(df: pd.DataFrame, target_col: str = "Price", windows: list[int] | None = None,) -> pd.DataFrame:
    df = df.copy()
    if windows is None:
        windows = [3, 6, 12, 24, 48]

    for window in windows:
        df[f"{target_col}_roll_mean_{window}"] = df[target_col].rolling(window=window).mean()
        df[f"{target_col}_roll_max_{window}"] = df[target_col].rolling(window=window).max()

    return df

def build_supervised_dataset(df: pd.DataFrame, horizon_steps: int,timestamp_col: str = "timestamp",target_col: str = "Price",) -> pd.DataFrame:
    df = df.copy()
    df = add_time_features(df, timestamp_col=timestamp_col)
    df = add_lag_features(df, target_col=target_col)
    df = add_rolling_features(df, target_col=target_col)
    df = add_weather_features(df)

    df["target_Price"] = df[target_col].shift(-horizon_steps)
    df = df.dropna().reset_index(drop=True)
    return df


def add_weather_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "temperature_c" not in df.columns:
        df["temperature_c"] = 0.0
    if "wind_speed_kph" not in df.columns:
        df["wind_speed_kph"] = 0.0
    if "humidity" not in df.columns:
        df["humidity"] = 0.0

    # normalize humidity to 0–1
    df["humidity"] =pd.to_numeric(df["humidity"], errors="coerce").astype("float64")
    df.loc[df["humidity"] > 1.0, "humidity"] = df.loc[df["humidity"] > 1.0, "humidity"] / 100.0

    if "feels_like_c" not in df.columns:
        df["feels_like_c"] = df["temperature_c"]
    if "precipitation_mm" not in df.columns:
        df["precipitation_mm"] = 0.0

    df["is_raining"] = (df["precipitation_mm"] > 0).astype(int)

    # simple HVAC-related transforms
    df["heating_degree"] = (18.0 - df["temperature_c"]).clip(lower=0)
    df["cooling_degree"] = (df["temperature_c"] - 22.0).clip(lower=0)

    df["temp_x_humidity"] = df["temperature_c"] * df["humidity"]
    df["feels_like_diff"] = df["feels_like_c"] - df["temperature_c"]

    return df

FEATURE_COLUMNS = [
    "hour",
    "day_of_week",
    "is_weekend",
    "is_workday",
    "is_monday",
    "is_friday",
    "is_business_hours",
    "is_peak_hours",
    "is_holiday",
    "is_day_before_holiday",
    "is_day_after_holiday",
    "hour_sin",
    "hour_cos",
    "dow_sin",
    "dow_cos",
    "month",
    "month_sin",
    "month_cos",
    "Price_lag_1",
    "Price_lag_3",
    "Price_lag_6",
    "Price_lag_12",
    "Price_lag_24",
    "Price_lag_48",
    "Price_lag_168",
    "Price_roll_mean_3",
    "Price_roll_max_3",
    "Price_roll_mean_6",
    "Price_roll_max_6",
    "Price_roll_mean_12",
    "Price_roll_max_12",
    "Price_roll_mean_24",
    "Price_roll_max_24",
    "Price_roll_mean_48",
    "Price_roll_max_48",
    "temperature_c",
    "wind_speed_kph",
    "heating_degree",
    "cooling_degree",
    "humidity",
    "feels_like_c",
    "precipitation_mm",
    "is_raining",
    "temp_x_humidity",
    "feels_like_diff",
]