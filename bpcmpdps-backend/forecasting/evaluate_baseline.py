from __future__ import annotations

import pandas as pd
from sklearn.metrics import mean_absolute_error, root_mean_squared_error


def evaluate_baseline_on_csv(
    csv_path: str,
    baseline: str = "yesterday",
) -> dict:
    """
    Evaluate a simple baseline on the provided CSV.

    Supported baselines:
    - "yesterday": predict same hour yesterday (lag 24)
    - "last_week": predict same hour last week (lag 168)
    """
    df = pd.read_csv(csv_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)

    if "demand_kw" not in df.columns:
        raise ValueError("CSV must contain a 'demand_kw' column.")

    if baseline == "yesterday":
        lag = 24
    elif baseline == "last_week":
        lag = 168
    else:
        raise ValueError("baseline must be either 'yesterday' or 'last_week'")

    df["baseline_pred"] = df["demand_kw"].shift(lag)

    eval_df = df.dropna(subset=["baseline_pred", "demand_kw"]).copy()

    y_true = eval_df["demand_kw"]
    y_pred = eval_df["baseline_pred"]

    return {
        "baseline": baseline,
        "lag_hours": lag,
        "num_test_rows": int(len(eval_df)),
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "rmse": float(root_mean_squared_error(y_true, y_pred)),
    }


if __name__ == "__main__":
    csv_path = "forecasting/data/demand_weather_testing.csv"

    for baseline_name in ["yesterday", "last_week"]:
        result = evaluate_baseline_on_csv(csv_path, baseline=baseline_name)
        print(result)