"""Central configuration for paths and constants."""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Data paths
RAW_DATA_PATH = PROJECT_ROOT / "1_data" / "raw" / "telco_churn.csv"
PROCESSED_DATA_PATH = PROJECT_ROOT / "1_data" / "processed" / "cleaned_churn.csv"
FEATURES_PATH = PROJECT_ROOT / "1_data" / "processed" / "features.csv"

# Model paths
MODEL_PATH = PROJECT_ROOT / "5_model" / "churn_model.pkl"
METRICS_PATH = PROJECT_ROOT / "5_model" / "model_metrics.json"
ENCODER_PATH = PROJECT_ROOT / "5_model" / "encoders.pkl"
SCALER_PATH = PROJECT_ROOT / "5_model" / "scaler.pkl"

# Database
DB_PATH = PROJECT_ROOT / "8_database" / "churn.db"
SCHEMA_PATH = PROJECT_ROOT / "8_database" / "schema.sql"

# Logs
PIPELINE_LOG = PROJECT_ROOT / "14_logs" / "pipeline.log"
API_LOG = PROJECT_ROOT / "14_logs" / "api.log"

# Reports
REPORTS_DIR = PROJECT_ROOT / "11_reports"
CHARTS_DIR = REPORTS_DIR / "charts"

# Model settings
TARGET_COLUMN = "Churn"
TEST_SIZE = 0.2
RANDOM_STATE = 42

# API
API_HOST = "127.0.0.1"
API_PORT = 8000

# Risk thresholds
HIGH_RISK_THRESHOLD = 0.7
MEDIUM_RISK_THRESHOLD = 0.4

# Categorical columns for encoding
CATEGORICAL_COLUMNS = [
    "gender", "Partner", "Dependents", "PhoneService", "MultipleLines",
    "InternetService", "OnlineSecurity", "OnlineBackup", "DeviceProtection",
    "TechSupport", "StreamingTV", "StreamingMovies", "Contract",
    "PaperlessBilling", "PaymentMethod",
]

NUMERIC_COLUMNS = ["SeniorCitizen", "tenure", "MonthlyCharges", "TotalCharges"]
