from __future__ import annotations

from pathlib import Path
import duckdb

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "duckdb" / "sec_filings.duckdb"


def inspect_database() -> None:
    """Print a simple summary of the DuckDB database and its tables."""
    conn = duckdb.connect(str(DB_PATH))

    print("Database:", DB_PATH)
    print("--- Tables ---")
    for row in conn.execute("SHOW TABLES").fetchall():
        print(row[0])

    print("--- Documents summary ---")
    print(conn.execute("SELECT COUNT(*) AS document_count FROM documents").fetchall())

    print("--- Elements summary ---")
    print(conn.execute("SELECT COUNT(*) AS element_count FROM elements").fetchall())

    print("--- Sample rows ---")
    print(conn.execute("SELECT * FROM documents LIMIT 5").fetchdf())
    print(conn.execute("SELECT * FROM elements LIMIT 5").fetchdf())

    conn.close()


if __name__ == "__main__":
    inspect_database()
