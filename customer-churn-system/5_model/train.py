"""Train churn prediction model."""
import json
import logging
import pickle
import sys
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "12_config"))
import config

sys.path.insert(0, str(ROOT / "4_feature_engineering"))
from features import create_features, get_feature_columns
from encoding import encode_categoricals, save_encoders
from scaling import scale_features, save_scaler

logger = logging.getLogger(__name__)


def prepare_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series, list[str], dict, object]:
    """Prepare features and target for training."""
    df = create_features(df)

    cat_cols = [c for c in config.CATEGORICAL_COLUMNS if c in df.columns]
    df, encoders = encode_categoricals(df, cat_cols, fit=True)

    feature_cols = get_feature_columns(df)
    X = df[feature_cols]
    y = df[config.TARGET_COLUMN]

    X_scaled, scaler = scale_features(X, fit=True)
    return X_scaled, y, feature_cols, encoders, scaler


def train_model(df: pd.DataFrame | None = None) -> dict:
    """Train RandomForest classifier and save artifacts."""
    if df is None:
        df = pd.read_csv(config.PROCESSED_DATA_PATH)

    X, y, feature_cols, encoders, scaler = prepare_data(df)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=config.TEST_SIZE, random_state=config.RANDOM_STATE, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=12,
        random_state=config.RANDOM_STATE,
        class_weight="balanced",
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": round(float(accuracy_score(y_test, y_pred)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, y_proba)), 4),
        "classification_report": classification_report(y_test, y_pred, output_dict=True),
        "feature_columns": feature_cols,
    }

    config.MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(config.MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    save_encoders(encoders, config.ENCODER_PATH)
    save_scaler(scaler, config.SCALER_PATH)

    with open(config.METRICS_PATH, "w") as f:
        json.dump({k: v for k, v in metrics.items() if k != "classification_report"}, f, indent=2)

    logger.info("Model trained — accuracy: %.4f, ROC-AUC: %.4f", metrics["accuracy"], metrics["roc_auc"])
    return metrics


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print(train_model())
