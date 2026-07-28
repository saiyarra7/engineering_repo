CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY,
    filename TEXT NOT NULL,
    source_path TEXT NOT NULL,
    ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS elements (
    id INTEGER PRIMARY KEY,
    document_id INTEGER NOT NULL,
    element_index INTEGER NOT NULL,
    element_type TEXT NOT NULL,
    text TEXT,
    FOREIGN KEY (document_id) REFERENCES documents(id)
);

CREATE SEQUENCE IF NOT EXISTS documents_seq START 1;
CREATE SEQUENCE IF NOT EXISTS elements_seq START 1;
