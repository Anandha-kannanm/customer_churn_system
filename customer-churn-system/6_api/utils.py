"""API helper functions."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "12_config"))
import config

REQUIRED_FIELDS = [
    "gender", "SeniorCitizen", "Partner", "Dependents", "tenure",
    "PhoneService", "MultipleLines", "InternetService", "OnlineSecurity",
    "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV",
    "StreamingMovies", "Contract", "PaperlessBilling", "PaymentMethod",
    "MonthlyCharges", "TotalCharges",
]


def validate_customer_input(data: dict) -> tuple[bool, str]:
    """Validate incoming prediction request payload."""
    missing = [f for f in REQUIRED_FIELDS if f not in data]
    if missing:
        return False, f"Missing fields: {', '.join(missing)}"
    return True, ""


def format_prediction_response(result: dict, customer_id: str | None = None) -> dict:
    """Format prediction result for API response."""
    return {
        "customer_id": customer_id,
        "churn_probability": result["churn_probability"],
        "will_churn": result["will_churn"],
        "risk_level": result["risk_level"],
    }
