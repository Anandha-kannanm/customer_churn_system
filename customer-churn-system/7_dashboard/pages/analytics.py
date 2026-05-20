"""Dashboard analytics page."""
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "12_config"))
import config

sys.path.insert(0, str(ROOT / "5_model"))
from predict import predict_churn

sys.path.insert(0, str(ROOT / "9_business_logic"))
from risk_segmentation import segment_summary

st.header("Analytics")

df = pd.read_csv(config.PROCESSED_DATA_PATH)
sample = df.drop(columns=["customerID", "Churn"], errors="ignore").head(200)

with st.spinner("Running predictions on sample..."):
    results = predict_churn(sample)
    proba = [r["churn_probability"] for r in results]
    summary = segment_summary(pd.DataFrame({"churn_probability": proba}))

st.subheader("Risk Segment Distribution (Sample)")
for segment, data in summary.items():
    st.metric(segment, f"{data['count']} ({data['pct']}%)")

st.subheader("Churn by Contract Type")
if "Contract" in df.columns:
    churn_by_contract = df.groupby("Contract")["Churn"].mean()
    st.bar_chart(churn_by_contract)

st.subheader("Tenure vs Monthly Charges")
st.scatter_chart(df, x="tenure", y="MonthlyCharges", color="Churn")
