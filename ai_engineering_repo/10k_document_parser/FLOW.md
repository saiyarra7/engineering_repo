# 10-K Document Parser Flow

## What this project does

This project is a small local proof of concept for ingesting an SEC 10-K filing from disk, parsing it, and storing the extracted content in a DuckDB database.

It does only three things:

1. Load an SEC filing HTML file from disk
2. Parse the document into structured elements using sec-parser
3. Store the document metadata and parsed elements in DuckDB

No chunking, embeddings, vector search, or RAG logic is included.

## Project structure

- main.py - entry point for the full ingestion flow
- parser/parse_sec.py - wrapper around sec-parser for extracting elements
- duckdb/init_db.py - creates the DuckDB database and schema
- duckdb/schema.sql - SQL schema for the local database
- requirements.txt - Python dependencies
- README.md - quick start instructions

## End-to-end flow

### 1. Resolve input file
The script looks for an SEC filing in the repository data folder.

It first checks for:
- the provided local filing path, if passed in
- the copied filing under the repository data tree
- a fallback sample file

### 2. Prepare the input file
The pipeline copies the chosen filing into the repository data folder so the POC has a consistent local input location.

### 3. Parse the filing
The parser reads the HTML file and runs sec-parser over it.

For each parsed element, it extracts:
- the element index
- the element type/class
- the text content

Empty or blank elements are skipped.

### 4. Create the DuckDB database
The script creates a local DuckDB database at:

- data/duckdb/sec_filings.duckdb

It also creates the tables:
- documents
- elements

### 5. Insert the data
The pipeline inserts:
- one row into documents for the filing
- one row per parsed element into elements

### 6. Print a summary
The script prints a short summary to show the ingestion result, including:
- how many elements were parsed
- how many rows were inserted
- that the run completed

## Files and data locations

### Data folders
- data/raw/sec_filings - original SEC filing files
- data/filings - sample or working copy used by the POC
- data/duckdb - DuckDB database files

### Output database
The main output file is:

- data/duckdb/sec_filings.duckdb

## How it works in practice

When you run the script:

1. the database is created or reused
2. the filing is loaded from disk
3. sec-parser extracts structured elements
4. those elements are inserted into DuckDB
5. the script prints a short completion summary

## Notes

This is intentionally simple and local-only. It is meant as a proof of concept for ingestion and storage, not as a production-grade pipeline.
