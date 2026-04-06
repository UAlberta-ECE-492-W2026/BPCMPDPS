from __future__ import annotations

from pathlib import Path
import requests

import pandas as pd
from forecasting.build_training_dataset import fetch_open_meteo_hourly_history


OPEN_METEO_ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"


def load_Price_xlsx(input_path: str | Path, sheet_name: str | int = 0,) -> pd.DataFrame:
    """
    Expects columns:
        timestamp
        Price
    """
    df = pd.read_excel(input_path, sheet_name=sheet_name)

    expected = {"timestamp", "Price"}
    missing = expected - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df[["timestamp", "Price"]].copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="raise")
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    df = df.dropna(subset=["timestamp", "Price"])
    df = df.sort_values("timestamp").drop_duplicates(subset=["timestamp"]).reset_index(drop=True)
    return df

def merge_Price_and_weather( Price_df: pd.DataFrame,weather_df: pd.DataFrame,) -> pd.DataFrame:
    """
    Merges on local naive hourly timestamps.
    We intentionally do NOT interpolate DST gaps.
    """
    merged = Price_df.merge(weather_df, on="timestamp", how="left", validate="one_to_one")

    missing_weather = (
        merged["temperature_c"].isna().sum()
        + merged["wind_speed_kph"].isna().sum()
        + merged["humidity"].isna().sum()
        + merged["feels_like_c"].isna().sum()
        + merged["precipitation_mm"].isna().sum()
    )
    if missing_weather > 0:
        print(f"Warning: found {missing_weather} missing weather cells after merge.")

    return merged


def build_training_dataset(input_xlsx: str | Path,
    output_csv: str | Path,
    latitude: float,
    longitude: float,
    timezone_name: str = "America/Edmonton",
    sheet_name: str | int = 0,
) -> pd.DataFrame:
    Price_df = load_Price_xlsx(input_xlsx, sheet_name=sheet_name)

    start_date = Price_df["timestamp"].min().date().isoformat()
    end_date = Price_df["timestamp"].max().date().isoformat()

    print(f"Price rows: {len(Price_df)}")
    print(f"Date range: {start_date} to {end_date}")

    weather_df = fetch_open_meteo_hourly_history(
        latitude=latitude,
        longitude=longitude,
        start_date=start_date,
        end_date=end_date,
        timezone_name=timezone_name,
    )

    print(f"Weather rows: {len(weather_df)}")

    merged_df = merge_Price_and_weather(Price_df, weather_df)
    merged_df["timestamp"] = pd.to_datetime(merged_df["timestamp"])

    train_df = merged_df[merged_df["timestamp"] < "2025-01-01"]
    test_df = merged_df[merged_df["timestamp"] >= "2025-01-01"]

    output_dir = Path("data")
    output_dir.mkdir(parents=True, exist_ok=True)

    train_df.to_csv(output_dir / "Price_weather_training.csv", index=False)
    test_df.to_csv(output_dir / "Price_weather_testing.csv", index=False)

    print(f"Saved training: {len(train_df)} rows")
    print(f"Saved testing: {len(test_df)} rows")
    print(train_df.head())
    print(test_df.head())

    # output_path = Path(output_csv)
    # output_path.parent.mkdir(parents=True, exist_ok=True)
    # merged_df.to_csv(output_path, index=False)

    # print(f"Saved merged dataset to: {output_path}")
    # print(merged_df.head())
    # print(merged_df.tail())

    return merged_df


if __name__ == "__main__":
    # Replace these with your actual file path and building coordinates.
    # change to price data .csv

    input_xlsx ="C:\\Users\\ktgar\\Downloads\\PoolPriceValues_2020-2026.xlsx"
    output_csv = "data/Pricemonthly average_weather_training.csv"

    # Example: set to your building's coordinates
    latitude = 53.54087514959737
    longitude = -113.49119564477701

    build_training_dataset(
        input_xlsx=input_xlsx,
        output_csv=output_csv,
        latitude=latitude,
        longitude=longitude,
        timezone_name="America/Edmonton",
        sheet_name=0
    )
