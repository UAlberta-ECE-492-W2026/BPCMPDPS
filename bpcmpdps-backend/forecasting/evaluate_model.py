from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import mean_absolute_error, root_mean_squared_error

from django.conf import settings

from .feature_engineering import build_supervised_dataset, FEATURE_COLUMNS


def evaluate_model_on_csv(csv_path: str, horizon_steps: int = 12) -> dict:
    df = pd.read_csv(csv_path)
    dataset = build_supervised_dataset(df, horizon_steps=horizon_steps)

    X_test = dataset[FEATURE_COLUMNS]
    y_test = dataset["target_demand_kw"]

    model_path = (
        Path(settings.BASE_DIR)
        / "forecasting"
        / "artifacts"
        / f"demand_model_h{horizon_steps}.joblib"
    )

    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")

    model = joblib.load(model_path)
    y_pred = model.predict(X_test)

    return {
        "horizon_steps": horizon_steps,
        "num_test_rows": int(len(X_test)),
        "mae": float(mean_absolute_error(y_test, y_pred)),
        "rmse": float(root_mean_squared_error(y_test, y_pred)),
    }