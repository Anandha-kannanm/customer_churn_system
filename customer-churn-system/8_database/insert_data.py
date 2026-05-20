"""Insert prediction results into database."""
import logging
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "12_config"))
import config

sys.path.insert(0, str(ROOT / "8_database"))
from db_connect import get_connection, init_database

logger = logging.getLogger(__name__)


def insert_predictions(predictions: list[dict]) -> int:
    """Insert batch of predictions into predictions table."""
    init_database()
    conn = get_connection()
    cursor = conn.cursor()

    count = 0
    for pred in predictions:
        cursor.execute(
            """INSERT INTO predictions (customerID, churn_probability, will_churn, risk_level)
               VALUES (?, ?, ?, ?)""",
            (
                pred.get("customerID"),
                pred.get("churn_probability"),
                int(pred.get("will_churn", 0)),
                pred.get("risk_level"),
            ),
        )
        count += 1

    conn.commit()
    conn.close()
    logger.info("Inserted %d predictions", count)
    return count


def batch_predict_from_csv(limit: int = 100) -> int:
    """Run predictions on processed data and store results."""
    sys.path.insert(0, str(ROOT / "5_model"))
    from predict import predict_churn

    df = pd.read_csv(config.PROCESSED_DATA_PATH).head(limit)
    customer_ids = df["customerID"].tolist()
    df_input = df.drop(columns=["customerID", "Churn"], errors="ignore")

    # Re-map binary columns back to strings for predict pipeline
    reverse_binary = {
        "Partner": {1: "Yes", 0: "No"}, "Dependents": {1: "Yes", 0: "No"},
        "PhoneService": {1: "Yes", 0: "No"}, "PaperlessBilling": {1: "Yes", 0: "No"},
    }
    for col, mapping in reverse_binary.items():
        if col in df_input.columns:
            df_input[col] = df_input[col].map(mapping)

    results = predict_churn(df_input)
    predictions = []
    for cid, res in zip(customer_ids, results):
        predictions.append({"customerID": cid, **res})

    return insert_predictions(predictions)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print(f"Inserted {batch_predict_from_csv()} predictions")
