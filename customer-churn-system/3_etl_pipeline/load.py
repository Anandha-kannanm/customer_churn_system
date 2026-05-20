"""Save data into SQLite database."""
import logging
import sqlite3
import pandas as pd

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "12_config"))
import config
DB_PATH = config.DB_PATH
SCHEMA_PATH = config.SCHEMA_PATH

logger = logging.getLogger(__name__)


def init_db(conn: sqlite3.Connection) -> None:
    """Create tables from schema.sql."""
    if SCHEMA_PATH.exists():
        with open(SCHEMA_PATH) as f:
            conn.executescript(f.read())
    conn.commit()


def load_customers(df: pd.DataFrame, db_path: Path | None = None) -> int:
    """Insert cleaned customer records into database."""
    path = db_path or DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(path)
    init_db(conn)

    # Select columns that match schema
    cols = [
        "customerID", "gender", "SeniorCitizen", "Partner", "Dependents",
        "tenure", "PhoneService", "InternetService", "Contract",
        "PaymentMethod", "MonthlyCharges", "TotalCharges", "Churn",
    ]
    available = [c for c in cols if c in df.columns]
    load_df = df[available].copy()
    load_df["Churn"] = load_df["Churn"].astype(int)

    load_df.to_sql("customers", conn, if_exists="replace", index=False)
    count = len(load_df)
    conn.close()
    logger.info("Loaded %d records into %s", count, path)
    return count
