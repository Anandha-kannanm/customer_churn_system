"""Feature creation logic for model training."""
import pandas as pd
import numpy as np


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """Build model-ready features from cleaned data."""
    df = df.copy()

    if "AvgMonthlyCharge" not in df.columns:
        df["AvgMonthlyCharge"] = df["TotalCharges"] / df["tenure"].replace(0, 1)

    if "HasInternet" not in df.columns:
        df["HasInternet"] = (df["InternetService"] != "No").astype(int)

    if "HasStreaming" not in df.columns:
        df["HasStreaming"] = ((df.get("StreamingTV", 0) == 1) | (df.get("StreamingMovies", 0) == 1)).astype(int)

    # Contract risk score
    contract_map = {"Month-to-month": 3, "One year": 2, "Two year": 1}
    df["ContractRisk"] = df["Contract"].map(contract_map).fillna(2)

    # Tenure buckets as numeric
    tenure_map = {"0-12": 1, "13-24": 2, "25-48": 3, "49-72": 4}
    if "TenureGroup" in df.columns:
        df["TenureGroupNum"] = df["TenureGroup"].map(tenure_map).fillna(1)
    else:
        df["TenureGroupNum"] = pd.cut(df["tenure"], bins=[0, 12, 24, 48, 72], labels=[1, 2, 3, 4]).astype(float)

    # Charge ratio feature
    df["ChargeRatio"] = df["MonthlyCharges"] / (df["AvgMonthlyCharge"] + 1)

    return df


def get_feature_columns(df: pd.DataFrame) -> list[str]:
    """Return columns used for model training."""
    exclude = {"customerID", "Churn", "TenureGroup"}
    numeric = df.select_dtypes(include=[np.number]).columns.tolist()
    return [c for c in numeric if c not in exclude]
