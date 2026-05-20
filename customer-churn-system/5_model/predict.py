"""Prediction script for churn model."""
import pickle
import sys
from pathlib import Path

import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "12_config"))
import config

sys.path.insert(0, str(ROOT / "4_feature_engineering"))
from features import create_features, get_feature_columns
from encoding import encode_categoricals, load_encoders
from scaling import load_scaler


def load_model():
    with open(config.MODEL_PATH, "rb") as f:
        return pickle.load(f)


def predict_churn(customer_data: dict | pd.DataFrame) -> list[dict]:
    """Predict churn probability for one or more customers."""
    model = load_model()
    encoders = load_encoders(config.ENCODER_PATH)
    scaler = load_scaler(config.SCALER_PATH)

    if isinstance(customer_data, dict):
        df = pd.DataFrame([customer_data])
    else:
        df = customer_data.copy()

    with open(config.METRICS_PATH) as f:
        import json
        metrics = json.load(f)
    feature_cols = metrics.get("feature_columns", [])

    df = create_features(df)
    cat_cols = [c for c in config.CATEGORICAL_COLUMNS if c in df.columns]
    df, _ = encode_categoricals(df, cat_cols, fit=False, encoders=encoders)

    for col in feature_cols:
        if col not in df.columns:
            df[col] = 0

    X = df[feature_cols]
    X_scaled = pd.DataFrame(scaler.transform(X), columns=feature_cols)

    proba = model.predict_proba(X_scaled)[:, 1]
    preds = model.predict(X_scaled)

    results = []
    for i in range(len(df)):
        results.append({
            "churn_probability": round(float(proba[i]), 4),
            "will_churn": bool(preds[i]),
            "risk_level": _risk_level(proba[i]),
        })
    return results


def _risk_level(proba: float) -> str:
    if proba >= config.HIGH_RISK_THRESHOLD:
        return "High"
    if proba >= config.MEDIUM_RISK_THRESHOLD:
        return "Medium"
    return "Low"


if __name__ == "__main__":
    sample = {
        "gender": "Female", "SeniorCitizen": 0, "Partner": "Yes", "Dependents": "No",
        "tenure": 1, "PhoneService": "No", "MultipleLines": "No phone service",
        "InternetService": "DSL", "OnlineSecurity": "No", "OnlineBackup": "Yes",
        "DeviceProtection": "No", "TechSupport": "No", "StreamingTV": "No",
        "StreamingMovies": "No", "Contract": "Month-to-month",
        "PaperlessBilling": "Yes", "PaymentMethod": "Electronic check",
        "MonthlyCharges": 29.85, "TotalCharges": 29.85,
    }
    print(predict_churn(sample))
