-- Attach the database file first so the queries run against the correct DuckDB file.
ATTACH 'C:/Users/Sai Yarra/Documents/tech_projects 2026/engineering-repo/ai_engineering_repo/data/duckdb/sec_filings.duckdb' AS sec_data (READ_ONLY);
USE sec_data;

-- Inspect available tables
SHOW TABLES;

-- Inspect available databases
SHOW DATABASES;

-- Count rows in the main tables
SELECT 'documents' AS table_name, COUNT(*) AS row_count
FROM documents
UNION ALL
SELECT 'elements' AS table_name, COUNT(*) AS row_count
FROM elements;

-- Preview document metadata
SELECT *
FROM documents
LIMIT 10;

-- Preview parsed elements
SELECT *
FROM elements
LIMIT 20;

-- Group elements by type
SELECT element_type, COUNT(*) AS row_count
FROM elements
GROUP BY element_type
ORDER BY row_count DESC
LIMIT 20;

-- Search for business-related text
SELECT *
FROM elements
WHERE text ILIKE '%business%'
LIMIT 20;
