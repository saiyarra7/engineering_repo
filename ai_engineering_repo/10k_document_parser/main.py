from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import shutil
import sys

PROJECT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PROJECT_ROOT.parent
SUPPORT_ROOT = PROJECT_ROOT / "db_support"

if str(PROJECT_ROOT) in sys.path:
    sys.path.remove(str(PROJECT_ROOT))

import duckdb
from duckdb import Error as DuckDBError

sys.path.insert(0, str(PROJECT_ROOT))

init_db_spec = spec_from_file_location("sec_duckdb_init", PROJECT_ROOT / "db_support" / "init_db.py")
if init_db_spec is None or init_db_spec.loader is None:
    raise ImportError("Unable to load DuckDB initialization module")

init_db_module = module_from_spec(init_db_spec)
init_db_spec.loader.exec_module(init_db_module)
create_database = init_db_module.create_database

parse_sec_spec = spec_from_file_location("sec_parse_module", PROJECT_ROOT / "parser" / "parse_sec.py")
if parse_sec_spec is None or parse_sec_spec.loader is None:
    raise ImportError("Unable to load SEC parser module")

parse_sec_module = module_from_spec(parse_sec_spec)
parse_sec_spec.loader.exec_module(parse_sec_module)
parse_html = parse_sec_module.parse_html


DATA_DIR = REPO_ROOT / "data" / "filings"
SAMPLE_FILE = DATA_DIR / "sample_10k.html"
DATA_ROOT = REPO_ROOT / "data"
DB_PATH = DATA_ROOT / "duckdb" / "sec_filings.duckdb"
DEFAULT_INPUT_FILE = REPO_ROOT / "data" / "raw" / "sec_filings" / "lly-10k-20251231.html"


def resolve_input_file(custom_path: str | None = None) -> Path:
    """Resolve the SEC filing path, preferring the provided local file if it exists."""
    if custom_path:
        candidate = Path(custom_path).expanduser()
        if candidate.exists():
            return candidate
        raise FileNotFoundError(f"Input file not found: {candidate}")

    if DEFAULT_INPUT_FILE.exists():
        return DEFAULT_INPUT_FILE

    if SAMPLE_FILE.exists():
        return SAMPLE_FILE

    raise FileNotFoundError("No SEC filing found. Provide a path to an HTML filing.")


def prepare_input_file(input_path: Path) -> Path:
    """Copy the filing into the local sample path for the POC."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if input_path == SAMPLE_FILE:
        return SAMPLE_FILE

    shutil.copyfile(input_path, SAMPLE_FILE)
    return SAMPLE_FILE


def insert_document(conn, filename: str, source_path: str) -> int:
    """Insert a document record and return its generated id."""
    max_id = conn.execute("SELECT COALESCE(MAX(id), 0) FROM documents").fetchone()[0]
    document_id = int(max_id) + 1
    conn.execute(
        """
        INSERT INTO documents (id, filename, source_path)
        VALUES (?, ?, ?)
        """,
        (document_id, filename, source_path),
    )
    return document_id


def insert_elements(conn, document_id: int, elements: list[dict[str, object]]) -> int:
    """Insert all parsed elements for a document."""
    if not elements:
        return 0

    max_id = conn.execute("SELECT COALESCE(MAX(id), 0) FROM elements").fetchone()[0]
    next_id = int(max_id) + 1

    for item in elements:
        conn.execute(
            """
            INSERT INTO elements (id, document_id, element_index, element_type, text)
            VALUES (?, ?, ?, ?, ?)
            """,
            (next_id, document_id, item["element_index"], item["element_type"], item["text"]),
        )
        next_id += 1

    return len(elements)


def main() -> None:
    """Run the ingestion pipeline from local HTML to DuckDB."""
    try:
        conn = create_database(DB_PATH)
        print("Database initialized")

        input_path = resolve_input_file(sys.argv[1] if len(sys.argv) > 1 else None)
        local_file = prepare_input_file(input_path)
        print(f"Loaded {local_file.name}")

        parsed_elements = parse_html(local_file)
        print(f"Parsed {len(parsed_elements)} elements")

        document_id = insert_document(conn, SAMPLE_FILE.name, str(SAMPLE_FILE))
        print("Inserted document")

        inserted_rows = insert_elements(conn, document_id, parsed_elements)
        print(f"Inserted {inserted_rows} rows")
        conn.commit()
        print("Done")

    except FileNotFoundError as exc:
        print(f"Error: {exc}")
        sys.exit(1)
    except RuntimeError as exc:
        print(f"Error: {exc}")
        sys.exit(1)
    except DuckDBError as exc:
        print(f"Database error: {exc}")
        sys.exit(1)
    finally:
        if "conn" in locals():
            conn.close()


if __name__ == "__main__":
    main()
