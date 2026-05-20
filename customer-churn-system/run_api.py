"""
Start the FastAPI server (Swagger docs at /docs).

Usage:
    python run_api.py
    python run_api.py --port 8000
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "12_config"))
sys.path.insert(0, str(ROOT / "6_api"))
sys.path.insert(0, str(ROOT / "5_model"))
sys.path.insert(0, str(ROOT / "9_business_logic"))

import config
from app import app

if __name__ == "__main__":
    import uvicorn

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=config.API_PORT)
    args = parser.parse_args()

    print(f"\n  API docs:  http://{args.host}:{args.port}/docs")
    print(f"  ReDoc:     http://{args.host}:{args.port}/redoc")
    print(f"  Health:    http://{args.host}:{args.port}/api/v1/health\n")

    uvicorn.run(app, host=args.host, port=args.port, reload=False)
