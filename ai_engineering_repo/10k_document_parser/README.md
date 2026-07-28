# 10-K Document Parser

This project is a small local proof of concept for ingesting an SEC 10-K filing from disk, parsing it with sec-parser, and storing the extracted elements in a local DuckDB database.

## Project structure

- data/filings/ - working sample copy of an SEC filing
- data/raw/sec_filings/ - original SEC filing files and related assets
- data/duckdb/ - DuckDB database output
- parser/parse_sec.py - parsing logic
- duckdb/init_db.py - DuckDB database and schema setup
- duckdb/schema.sql - SQL schema for the local database
- main.py - entry point for the ingestion pipeline
- FLOW.md - end-to-end explanation of the ingestion flow
- requirements.txt - Python dependencies

## Installation

From the project directory, install the dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Expected output

The script will:

1. Create or reuse a local DuckDB database at data/duckdb/sec_filings.duckdb
2. Create the required tables
3. Load a filing from the repository data folder
4. Parse the filing and extract structured elements
5. Insert document metadata and elements into DuckDB

You should see output similar to:

```text
Database initialized
Loaded sample_10k.html
Parsed X elements
Inserted document
Inserted X rows
Done
```
