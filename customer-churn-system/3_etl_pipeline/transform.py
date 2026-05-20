"""Data cleaning and basic feature engineering."""
import logging
import pandas as pd
import numpy as np

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "12_config"))
import config
PROCESSED_DATA_PATH = config.PROCESSED_DATA_PATH

logger = logging.getLogger(__name__)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and prepare raw telco churn data."""
    df = df.copy()

    # Drop duplicate customer IDs
    df = df.drop_duplicates(subset=["customerID"], keep="first")

    # Fix TotalCharges (stored as object with blanks)
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df["TotalCharges"] = df["TotalCharges"].fillna(df["MonthlyCharges"])

    # Standardize Churn target
    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

    # SeniorCitizen already 0/1
    df["SeniorCitizen"] = df["SeniorCitizen"].astype(int)

    # Binary yes/no columns
    binary_cols = [
        "Partner", "Dependents", "PhoneService", "PaperlessBilling",
        "OnlineSecurity", "OnlineBackup", "DeviceProtection",
        "TechSupport", "StreamingTV", "StreamingMovies",
    ]
    for col in binary_cols:
        if col in df.columns:
            df[col] = df[col].replace({"Yes": 1, "No": 0, "No internet service": 0, "No phone service": 0})

    # Feature engineering
    df["AvgMonthlyCharge"] = df["TotalCharges"] / df["tenure"].replace(0, 1)
    df["HasInternet"] = (df["InternetService"] != "No").astype(int)
    df["HasStreaming"] = ((df["StreamingTV"] == 1) | (df["StreamingMovies"] == 1)).astype(int)
    df["TenureGroup"] = pd.cut(
        df["tenure"],
        bins=[0, 12, 24, 48, 72],
        labels=["0-12", "13-24", "25-48", "49-72"],
    ).astype(str)

    logger.info("Cleaned data: %d rows", len(df))
    return df


def transform(df: pd.DataFrame, save: bool = True) -> pd.DataFrame:
    """Run full transform pipeline."""
    cleaned = clean_data(df)
    if save:
        PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        cleaned.to_csv(PROCESSED_DATA_PATH, index=False)
        logger.info("Saved processed data to %s", PROCESSED_DATA_PATH)
    return cleaned
