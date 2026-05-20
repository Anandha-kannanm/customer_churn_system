"""
Open Jupyter notebooks in the browser.

Usage:
    python run_notebooks.py
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
notebooks = ROOT / "2_notebooks"

if __name__ == "__main__":
    print(f"\n  Notebooks folder: {notebooks}")
    print("  Jupyter will open in your browser (http://localhost:8888)")
    print("  Press Ctrl+C once to stop.\n")
    try:
        subprocess.run(
            [sys.executable, "-m", "notebook", str(notebooks)],
            cwd=str(ROOT),
        )
    except KeyboardInterrupt:
        print("\nJupyter stopped.")
