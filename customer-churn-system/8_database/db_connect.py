"""Database connection setup."""
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "12_config"))
import config


def get_connection(db_path: Path | None = None) -> sqlite3.Connection:
    """Return SQLite connection with row factory."""
    path = db_path or config.DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_database() -> None:
    """Initialize database schema."""
    conn = get_connection()
    with open(config.SCHEMA_PATH) as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
