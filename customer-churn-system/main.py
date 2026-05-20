"""
Customer Churn System — main entry point.

Usage:
    python main.py              # Run full pipeline (ETL + train + DB)
    python main.py --etl        # ETL only
    python main.py --train      # Train model only
    python main.py --api        # Start FastAPI server
    python main.py --dashboard  # Start Streamlit dashboard
"""
import argparse
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "12_config"))
sys.path.insert(0, str(ROOT / "3_etl_pipeline"))
sys.path.insert(0, str(ROOT / "5_model"))
sys.path.insert(0, str(ROOT / "8_database"))

import config


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )


def run_etl():
    from pipeline_runner import run_pipeline
    return run_pipeline()


def run_train():
    from train import train_model
    return train_model()


def run_db_predictions():
    from insert_data import batch_predict_from_csv
    return batch_predict_from_csv()


def run_api():
    """Start API server — Swagger docs at http://127.0.0.1:8000/docs"""
    import subprocess
    subprocess.run([sys.executable, str(ROOT / "run_api.py")])


def run_dashboard():
    import subprocess
    print("\n  Dashboard:  http://localhost:8501")
    print("  Press Ctrl+C to stop.\n")
    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run",
             str(ROOT / "7_dashboard" / "streamlit_app.py"), "--server.port", "8501"],
            cwd=str(ROOT),
        )
    except KeyboardInterrupt:
        print("\nDashboard stopped.")


def main():
    parser = argparse.ArgumentParser(description="Customer Churn Prediction System")
    parser.add_argument("--etl", action="store_true", help="Run ETL pipeline only")
    parser.add_argument("--train", action="store_true", help="Train model only")
    parser.add_argument("--api", action="store_true", help="Start API server")
    parser.add_argument("--dashboard", action="store_true", help="Start Streamlit dashboard")
    parser.add_argument("--predictions", action="store_true", help="Batch predict and store in DB")
    args = parser.parse_args()

    setup_logging()

    if args.api:
        run_api()
    elif args.dashboard:
        run_dashboard()
    elif args.etl:
        run_etl()
    elif args.train:
        run_train()
    elif args.predictions:
        run_db_predictions()
    else:
        logging.info("Running full pipeline...")
        run_etl()
        metrics = run_train()
        logging.info("Training complete: %s", metrics)
        count = run_db_predictions()
        logging.info("Stored %d predictions in database", count)
        logging.info("Done! Start API: python main.py --api | Dashboard: python main.py --dashboard")


if __name__ == "__main__":
    main()
