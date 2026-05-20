"""Pydantic schemas for API request/response (Swagger docs)."""
from pydantic import BaseModel, Field
from typing import Optional


class CustomerInput(BaseModel):
    customerID: Optional[str] = Field(None, example="7590-VHVEG")
    gender: str = Field(..., example="Female")
    SeniorCitizen: int = Field(..., ge=0, le=1, example=0)
    Partner: str = Field(..., example="Yes")
    Dependents: str = Field(..., example="No")
    tenure: int = Field(..., ge=0, example=12)
    PhoneService: str = Field(..., example="Yes")
    MultipleLines: str = Field(..., example="No")
    InternetService: str = Field(..., example="DSL")
    OnlineSecurity: str = Field(..., example="No")
    OnlineBackup: str = Field(..., example="Yes")
    DeviceProtection: str = Field(..., example="No")
    TechSupport: str = Field(..., example="No")
    StreamingTV: str = Field(..., example="No")
    StreamingMovies: str = Field(..., example="No")
    Contract: str = Field(..., example="Month-to-month")
    PaperlessBilling: str = Field(..., example="Yes")
    PaymentMethod: str = Field(..., example="Electronic check")
    MonthlyCharges: float = Field(..., ge=0, example=65.5)
    TotalCharges: float = Field(..., ge=0, example=500.0)

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "gender": "Female",
                "SeniorCitizen": 0,
                "Partner": "Yes",
                "Dependents": "No",
                "tenure": 1,
                "PhoneService": "No",
                "MultipleLines": "No phone service",
                "InternetService": "DSL",
                "OnlineSecurity": "No",
                "OnlineBackup": "Yes",
                "DeviceProtection": "No",
                "TechSupport": "No",
                "StreamingTV": "No",
                "StreamingMovies": "No",
                "Contract": "Month-to-month",
                "PaperlessBilling": "Yes",
                "PaymentMethod": "Electronic check",
                "MonthlyCharges": 29.85,
                "TotalCharges": 29.85,
            }]
        }
    }


class RetentionActionOut(BaseModel):
    action: str
    priority: str
    message: str


class PredictionResponse(BaseModel):
    customer_id: Optional[str] = None
    churn_probability: float
    will_churn: bool
    risk_level: str
    retention_actions: Optional[list[RetentionActionOut]] = None


class HealthResponse(BaseModel):
    status: str
    service: str


class MetricsResponse(BaseModel):
    accuracy: float
    roc_auc: float
    feature_columns: list[str]
