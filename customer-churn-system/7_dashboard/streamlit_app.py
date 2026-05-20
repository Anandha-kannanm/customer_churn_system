"""Streamlit dashboard main entry."""
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "7_dashboard"))

st.set_page_config(
    page_title="Customer Churn Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Customer Churn Prediction System")
st.markdown("Monitor churn risk, run predictions, and analyze customer segments.")

overview = st.Page("pages/overview.py", title="Overview", icon="🏠")
prediction = st.Page("pages/prediction.py", title="Prediction", icon="🔮")
analytics = st.Page("pages/analytics.py", title="Analytics", icon="📈")

pg = st.navigation([overview, prediction, analytics])
pg.run()
