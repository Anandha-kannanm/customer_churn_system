"""Run full ETL pipeline: extract -> transform -> load."""
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "12_config"))
sys.path.insert(0, str(ROOT / "3_etl_pipeline"))
import config
from extract import extract
from transform import transform
from load import load_customers

PIPELINE_LOG = config.PIPELINE_LOG

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(PIPELINE_LOG),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


def run_pipeline() -> dict:
    """Execute complete ETL pipeline."""
    logger.info("Starting ETL pipeline")
    raw_df = extract()
    cleaned_df = transform(raw_df)
    row_count = load_customers(cleaned_df)
    logger.info("ETL pipeline complete")
    return {"rows_extracted": len(raw_df), "rows_loaded": row_count}


if __name__ == "__main__":
    result = run_pipeline()
    print(result)
