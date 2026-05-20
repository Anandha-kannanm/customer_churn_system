"""Load raw data from CSV."""
import logging
import pandas as pd

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "12_config"))
import config
RAW_DATA_PATH = config.RAW_DATA_PATH

logger = logging.getLogger(__name__)


def extract(file_path: Path | None = None) -> pd.DataFrame:
    """Load telco churn dataset from CSV."""
    path = file_path or RAW_DATA_PATH
    logger.info("Extracting data from %s", path)
    df = pd.read_csv(path)
    logger.info("Loaded %d rows, %d columns", len(df), len(df.columns))
    return df


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    df = extract()
    print(df.shape)
    print(df.head())
