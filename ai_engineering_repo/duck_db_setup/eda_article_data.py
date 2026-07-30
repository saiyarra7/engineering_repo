from pathlib import Path
import duckdb

# 1. Point to your updated local database file
DB_PATH = Path(r"C:\Users\Sai Yarra\Documents\tech_projects 2026\data\news_articles.duckdb")

if not DB_PATH.exists():
    raise FileNotFoundError(f"Database file not found at {DB_PATH}. Run the ingest pipeline first.")

# 2. Open connection to DuckDB
con = duckdb.connect(database=str(DB_PATH))

#EDA using sql

print("--- 1. SCHEMA INSPECTION ---")
con.sql("DESCRIBE articles;").show()


print("\n--- 2. DATASET VOLUME ---")
con.sql("""
    SELECT 
        *
    FROM articles;
""").show()


# Always close the file lock handle when finished
con.close()