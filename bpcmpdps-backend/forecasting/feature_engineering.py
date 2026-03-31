from __future__ import annotations

import pandas as pd
import math
import holidays


def add_time_features(df: pd.DataFrame, timestamp_col: str = "timestamp") -> pd.DataFrame:
    df = df.copy()
    ts = pd.to_datetime(df[timestamp_col])

    df["hour"] = ts.dt.hour
    df["day_of_week"] = ts.dt.dayofweek
    df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)
    df["is_workday"] = (df["day_of_week"] < 5).astype(int)
    df["is_monday"] = (df["day_of_week"] == 0).astype(int)
    df["is_friday"] = (df["day_of_week"] == 4).astype(int)

    df["is_business_hours"] = ((df["hour"] >= 8) & (df["hour"] < 18)).astype(int)
    df["is_peak_hours"] = ((df["hour"] >= 9) & (df["hour"] < 16)).astype(int)

    # Canadian holidays (Alberta)
    ca_holidays = holidays.CA(prov="AB")

    dates = ts.dt.normalize()

    df["is_holiday"] = dates.map(lambda d: 1 if d.date() in ca_holidays else 0)

    df["is_day_before_holiday"] = dates.map(
        lambda d: 1 if (d + pd.Timedelta(days=1)).date() in ca_holidays else 0
    )

    df["is_day_after_holiday"] = dates.map(
        lambda d: 1 if (d - pd.Timedelta(days=1)).date() in ca_holidays else 0
    )

    # cyclical encoding
    df["hour_sin"] = pd.Series(ts.dt.hour).map(lambda h: math.sin(2 * math.pi * h / 24))
    df["hour_cos"] = pd.Series(ts.dt.hour).map(lambda h: math.cos(2 * math.pi * h / 24))
    df["dow_sin"] = pd.Series(ts.dt.dayofweek).map(lambda d: math.sin(2 * math.pi * d / 7))
    df["dow_cos"] = pd.Series(ts.dt.dayofweek).map(lambda d: math.cos(2 * math.pi * d / 7))
    
    df["month"] = ts.dt.month
    df["month_sin"] = df["month"].map(lambda m: math.sin(2 * math.pi * m / 12))
    df["month_cos"] = df["month"].map(lambda m: math.cos(2 * math.pi * m / 12))
    
    return df


def add_lag_features(
    df: pd.DataFrame,
    target_col: str = "demand_kw",
    lags: list[int] | None = None,
) -> pd.DataFrame:
    df = df.copy()
    if lags is None:
        lags = [1, 3, 6, 12, 24, 48, 168]

    for lag in lags:
        df[f"{target_col}_lag_{lag}"] = df[target_col].shift(lag)

    return df


def add_rolling_features(
    df: pd.DataFrame,
    target_col: str = "demand_kw",
    windows: list[int] | None = None,
) -> pd.DataFrame:
    df = df.copy()
    if windows is None:
        windows = [3, 6, 12, 24, 48]

    for window in windows:
        df[f"{target_col}_roll_mean_{window}"] = df[target_col].rolling(window=window).mean()
        df[f"{target_col}_roll_max_{window}"] = df[target_col].rolling(window=window).max()

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
    df["humidity"] = pd.to_numeric(df["humidity"], errors="coerce")
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


def build_supervised_dataset(
    df: pd.DataFrame,
    horizon_steps: int,
    timestamp_col: str = "timestamp",
    target_col: str = "demand_kw",
) -> pd.DataFrame:
    df = df.copy()
    df = add_time_features(df, timestamp_col=timestamp_col)
    df = add_lag_features(df, target_col=target_col)
    df = add_rolling_features(df, target_col=target_col)
    df = add_weather_features(df)

    df["target_demand_kw"] = df[target_col].shift(-horizon_steps)
    df = df.dropna().reset_index(drop=True)
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
    "demand_kw_lag_1",
    "demand_kw_lag_3",
    "demand_kw_lag_6",
    "demand_kw_lag_12",
    "demand_kw_lag_24",
    "demand_kw_lag_48",
    "demand_kw_lag_168",
    "demand_kw_roll_mean_3",
    "demand_kw_roll_max_3",
    "demand_kw_roll_mean_6",
    "demand_kw_roll_max_6",
    "demand_kw_roll_mean_12",
    "demand_kw_roll_max_12",
    "demand_kw_roll_mean_24",
    "demand_kw_roll_max_24",
    "demand_kw_roll_mean_48",
    "demand_kw_roll_max_48",
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