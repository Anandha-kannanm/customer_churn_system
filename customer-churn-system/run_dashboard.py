"""
Start the Streamlit dashboard.

Usage:
    python run_dashboard.py
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
app = ROOT / "7_dashboard" / "streamlit_app.py"

if __name__ == "__main__":
    print("\n  Dashboard:  http://localhost:8501\n")
    print("  Press Ctrl+C to stop.\n")
    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", str(app), "--server.port", "8501"],
            cwd=str(ROOT),
        )
    except KeyboardInterrupt:
        print("\nDashboard stopped.")
