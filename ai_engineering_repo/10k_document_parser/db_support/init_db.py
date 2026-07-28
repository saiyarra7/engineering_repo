from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
for entry in list(sys.path):
    try:
        if entry and Path(entry).resolve() == PROJECT_ROOT:
            sys.path.remove(entry)
    except (FileNotFoundError, OSError, RuntimeError):
        continue

import duckdb


def create_database(db_path: Path) -> duckdb.DuckDBPyConnection:
    """Create the local DuckDB database and initialize the schema."""
    conn = duckdb.connect(str(db_path))

    schema_path = Path(__file__).with_name("schema.sql")
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    with schema_path.open("r", encoding="utf-8") as handle:
        conn.execute(handle.read())

    return conn
