"""Dashboard prediction page."""
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "5_model"))
from predict import predict_churn

st.header("Churn Prediction")

with st.form("predict_form"):
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("Gender", ["Male", "Female"])
        tenure = st.number_input("Tenure (months)", 0, 72, 12)
        contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
        internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
        monthly = st.number_input("Monthly Charges", 0.0, 200.0, 65.0)
    with col2:
        senior = st.selectbox("Senior Citizen", [0, 1])
        partner = st.selectbox("Partner", ["Yes", "No"])
        payment = st.selectbox("Payment Method", [
            "Electronic check", "Mailed check",
            "Bank transfer (automatic)", "Credit card (automatic)",
        ])
        phone = st.selectbox("Phone Service", ["Yes", "No"])
        total = st.number_input("Total Charges", 0.0, 10000.0, 500.0)

    submitted = st.form_submit_button("Predict Churn")

if submitted:
    customer = {
        "gender": gender, "SeniorCitizen": senior, "Partner": partner,
        "Dependents": "No", "tenure": tenure, "PhoneService": phone,
        "MultipleLines": "No", "InternetService": internet,
        "OnlineSecurity": "No", "OnlineBackup": "No",
        "DeviceProtection": "No", "TechSupport": "No",
        "StreamingTV": "No", "StreamingMovies": "No",
        "Contract": contract, "PaperlessBilling": "Yes",
        "PaymentMethod": payment, "MonthlyCharges": monthly,
        "TotalCharges": total,
    }
    result = predict_churn(customer)[0]
    risk_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
    st.success(f"Churn Probability: **{result['churn_probability']:.1%}**")
    st.info(f"Risk Level: {risk_color.get(result['risk_level'], '')} {result['risk_level']}")
    st.write(f"Will Churn: **{'Yes' if result['will_churn'] else 'No'}**")
