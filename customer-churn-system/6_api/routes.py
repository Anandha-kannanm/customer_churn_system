"""API route handlers."""
import json
import sys
from pathlib import Path

from fastapi import APIRouter, HTTPException

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "12_config"))
sys.path.insert(0, str(ROOT / "5_model"))
sys.path.insert(0, str(ROOT / "9_business_logic"))
sys.path.insert(0, str(ROOT / "6_api"))

import config
from predict import predict_churn
from churn_rules import get_retention_actions
from schemas import CustomerInput, PredictionResponse, HealthResponse, MetricsResponse, RetentionActionOut

router = APIRouter(tags=["Churn Prediction"])


@router.get("/health", response_model=HealthResponse, summary="Health check")
def health_check():
    return {"status": "healthy", "service": "churn-prediction-api"}


@router.post("/predict", response_model=PredictionResponse, summary="Predict customer churn")
def predict(data: CustomerInput):
    payload = data.model_dump(exclude_none=True)
    results = predict_churn(payload)
    result = results[0]

    response = PredictionResponse(
        customer_id=data.customerID,
        churn_probability=result["churn_probability"],
        will_churn=result["will_churn"],
        risk_level=result["risk_level"],
    )

    if data.customerID:
        actions = get_retention_actions(
            customer_id=data.customerID,
            churn_probability=result["churn_probability"],
            tenure=data.tenure,
            monthly_charges=data.MonthlyCharges,
            contract=data.Contract,
        )
        response.retention_actions = [
            RetentionActionOut(action=a.action, priority=a.priority, message=a.message)
            for a in actions
        ]

    return response


@router.get("/metrics", response_model=MetricsResponse, summary="Model performance metrics")
def get_metrics():
    if not config.METRICS_PATH.exists():
        raise HTTPException(status_code=404, detail="Model not trained yet. Run: python main.py --train")
    with open(config.METRICS_PATH) as f:
        data = json.load(f)
    return MetricsResponse(
        accuracy=data["accuracy"],
        roc_auc=data["roc_auc"],
        feature_columns=data.get("feature_columns", []),
    )
