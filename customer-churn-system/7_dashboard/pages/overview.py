"""Dashboard overview page."""
import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "12_config"))
import config

st.header("Overview")

df = pd.read_csv(config.PROCESSED_DATA_PATH)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Customers", f"{len(df):,}")
col2.metric("Churn Rate", f"{df['Churn'].mean():.1%}")
col3.metric("Avg Tenure", f"{df['tenure'].mean():.0f} mo")
col4.metric("Avg Monthly Charge", f"${df['MonthlyCharges'].mean():.2f}")

st.subheader("Churn Distribution")
churn_counts = df["Churn"].value_counts()
st.bar_chart(churn_counts.rename({0: "Retained", 1: "Churned"}))

if config.METRICS_PATH.exists():
    st.subheader("Model Performance")
    with open(config.METRICS_PATH) as f:
        metrics = json.load(f)
    m1, m2 = st.columns(2)
    m1.metric("Accuracy", metrics.get("accuracy", "N/A"))
    m2.metric("ROC-AUC", metrics.get("roc_auc", "N/A"))
else:
    st.info("Train the model first: `python main.py --train`")
