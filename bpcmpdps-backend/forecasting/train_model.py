from __future__ import annotations

import os
from pathlib import Path

import joblib
import pandas as pd
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error

from django.conf import settings

from .feature_engineering import build_supervised_dataset, FEATURE_COLUMNS


def train_and_save_model(
    df: pd.DataFrame,
    horizon_steps: int = 12,
    model_filename: str | None = None,
) -> dict:
    """
    Trains a basic demand model for a single forecast horizon and saves it.
    """
    dataset = build_supervised_dataset(df, horizon_steps=horizon_steps)

    X = dataset[FEATURE_COLUMNS]
    y = dataset["target_demand_kw"]

    # # CURRENT TESTING MODE:
    # split_date = "2025-01-01"   # train 2020–2024, test 2025

    # # FUTURE MODE (when 2025 can be included in training):
    # # split_date = "2026-01-01"

    # train = dataset[dataset["timestamp"] < split_date]
    # test = dataset[dataset["timestamp"] >= split_date]

    # print(f"Train rows: {len(train)}")
    # print(f"Test rows: {len(test)}")

    # X_train = train[FEATURE_COLUMNS]
    # y_train = train["target_demand_kw"]

    # X_test = test[FEATURE_COLUMNS]
    # y_test = test["target_demand_kw"]

    X_train = dataset[FEATURE_COLUMNS]
    y_train = dataset["target_demand_kw"]

    print(f"Train rows: {len(dataset)}")

    model = XGBRegressor(
        n_estimators=600,
        learning_rate=0.03,
        max_depth=8,
        min_child_weight=3,
        subsample=0.85,
        colsample_bytree=0.85,
        reg_alpha=0.1,
        reg_lambda=1.0,
        objective="reg:squarederror",
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    # y_pred = model.predict(X_test)
    # metrics = {
    #     "mae": float(mean_absolute_error(y_test, y_pred)),
    #     "rmse": float(root_mean_squared_error(y_test, y_pred)),
    #     "horizon_steps": horizon_steps,
    #     "num_train_rows": int(len(X_train)),
    #     "num_test_rows": int(len(X_test)),
    # }

    metrics = {
        "horizon_steps": horizon_steps,
        "num_train_rows": int(len(X_train)),
    }

    models_dir = Path(settings.BASE_DIR) / "forecasting" / "artifacts"
    models_dir.mkdir(parents=True, exist_ok=True)

    if model_filename is None:
        model_filename = f"demand_model_h{horizon_steps}.joblib"

    joblib.dump(model, models_dir / model_filename)
    return metrics


def load_csv_and_train(csv_path: str, horizon_steps: int = 12) -> dict:
    df = pd.read_csv(csv_path)
    return train_and_save_model(df, horizon_steps=horizon_steps)


if __name__ == "__main__":
    csv_path = os.environ.get("DEMAND_TRAINING_CSV")
    if not csv_path:
        raise RuntimeError("Set DEMAND_TRAINING_CSV to a CSV path before running this file directly.")

    result = load_csv_and_train(csv_path)
    print(result)