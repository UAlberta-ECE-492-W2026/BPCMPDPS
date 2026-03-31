from __future__ import annotations

from pathlib import Path
import requests
import pandas as pd


OPEN_METEO_ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"


def load_demand_xlsx(
    input_path: str | Path,
    sheet_name: str | int = 0,
) -> pd.DataFrame:
    """
    Expects columns:
        timestamp
        demand_kw
    """
    df = pd.read_excel(input_path, sheet_name=sheet_name)

    expected = {"timestamp", "demand_kw"}
    missing = expected - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df[["timestamp", "demand_kw"]].copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="raise")
    df["demand_kw"] = pd.to_numeric(df["demand_kw"], errors="coerce")
    df = df.dropna(subset=["timestamp", "demand_kw"])
    df = df.sort_values("timestamp").drop_duplicates(subset=["timestamp"]).reset_index(drop=True)
    return df


def fetch_open_meteo_hourly_history(
    latitude: float,
    longitude: float,
    start_date: str,
    end_date: str,
    timezone_name: str = "America/Edmonton",
) -> pd.DataFrame:
    """
    Fetches hourly historical weather from Open-Meteo.
    Returns columns:
        timestamp, temperature_c, wind_speed_kph, humidity, feels_like_c, precipitation_mm
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "temperature_2m,wind_speed_10m,relative_humidity_2m,apparent_temperature,precipitation",
        "timezone": timezone_name,
    }

    resp = requests.get(OPEN_METEO_ARCHIVE_URL, params=params, timeout=60)
    resp.raise_for_status()
    payload = resp.json()

    hourly = payload.get("hourly")
    if not hourly:
        raise RuntimeError(f"No hourly data returned: {payload}")

    weather_df = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(hourly["time"], errors="raise"),
            "temperature_c": hourly["temperature_2m"],
            "wind_speed_kph": hourly["wind_speed_10m"],
            "humidity": hourly.get("relative_humidity_2m"),
            "feels_like_c": hourly.get("apparent_temperature"),
            "precipitation_mm": hourly.get("precipitation"),
        }
    )

    weather_df["humidity"] = pd.to_numeric(weather_df["humidity"], errors="coerce")
    weather_df["feels_like_c"] = pd.to_numeric(weather_df["feels_like_c"], errors="coerce")
    weather_df["precipitation_mm"] = pd.to_numeric(weather_df["precipitation_mm"], errors="coerce")

    weather_df = weather_df.sort_values("timestamp").reset_index(drop=True)
    return weather_df


def merge_demand_and_weather(
    demand_df: pd.DataFrame,
    weather_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Merges on local naive hourly timestamps.
    We intentionally do NOT interpolate DST gaps.
    """
    merged = demand_df.merge(weather_df, on="timestamp", how="left", validate="one_to_one")

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


def build_training_dataset(
    input_xlsx: str | Path,
    # output_csv: str | Path,
    latitude: float,
    longitude: float,
    timezone_name: str = "America/Edmonton",
    sheet_name: str | int = 0,
) -> pd.DataFrame:
    demand_df = load_demand_xlsx(input_xlsx, sheet_name=sheet_name)

    start_date = demand_df["timestamp"].min().date().isoformat()
    end_date = demand_df["timestamp"].max().date().isoformat()

    print(f"Demand rows: {len(demand_df)}")
    print(f"Date range: {start_date} to {end_date}")

    weather_df = fetch_open_meteo_hourly_history(
        latitude=latitude,
        longitude=longitude,
        start_date=start_date,
        end_date=end_date,
        timezone_name=timezone_name,
    )

    print(f"Weather rows: {len(weather_df)}")

    merged_df = merge_demand_and_weather(demand_df, weather_df)
    merged_df["timestamp"] = pd.to_datetime(merged_df["timestamp"])

    train_df = merged_df[merged_df["timestamp"] < "2025-01-01"]
    test_df = merged_df[merged_df["timestamp"] >= "2025-01-01"]

    output_dir = Path("data")
    output_dir.mkdir(parents=True, exist_ok=True)

    train_df.to_csv(output_dir / "demand_weather_training.csv", index=False)
    test_df.to_csv(output_dir / "demand_weather_testing.csv", index=False)

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
    input_xlsx = "C:\\Users\\Abhi\\Desktop\\ECE492\\ATB_North_RTA_Jan_2020_to_Dec_2025.xlsx"
    # output_csv = "data/demand_weather_training.csv"

    # Example: set to your building's coordinates
    latitude = 53.54087514959737
    longitude = -113.49119564477701

    build_training_dataset(
        input_xlsx=input_xlsx,
        # output_csv=output_csv,
        latitude=latitude,
        longitude=longitude,
        timezone_name="America/Edmonton",
        sheet_name=0,
    )