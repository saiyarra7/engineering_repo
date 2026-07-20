from pathlib import Path
import duckdb

# 1. Point to your updated local database file
DB_PATH = Path(r"C:\Users\Sai Yarra\Documents\tech_projects 2026\data\sp500_company_data.duckdb")

if not DB_PATH.exists():
    raise FileNotFoundError(f"Database file not found at {DB_PATH}. Run the ingest pipeline first.")

# 2. Open connection to DuckDB
con = duckdb.connect(database=str(DB_PATH))

#EDA using sql

print("--- 1. SCHEMA INSPECTION ---")
con.sql("DESCRIBE sp500_company_data;").show()


print("\n--- 2. DATASET VOLUME ---")
con.sql("""
    SELECT 
        COUNT(*) as total_records,
        COUNT(DISTINCT Symbol) as unique_companies,
        COUNT(DISTINCT Sector) as unique_sectors
    FROM sp500_company_data;
""").show()


print("\n--- 3. NULL VALUE ANALYSIS ---")
con.sql("""
    SELECT 
        COUNT(*) - COUNT(Symbol) as missing_symbols,
        COUNT(*) - COUNT("Market Cap") as missing_market_caps,
        COUNT(*) - COUNT("Earnings/Share") as missing_eps,
        COUNT(*) - COUNT("Price/Earnings") as missing_pe
    FROM sp500_company_data;
""").show()


print("\n--- 4. TOP 10 LARGEST COMPANIES BY MARKET CAP ---")
con.sql("""
    SELECT 
        Symbol, 
        Name, 
        Sector, 
        "Market Cap", 
        "Price/Earnings" as PE_Ratio
    FROM sp500_company_data
    WHERE "Market Cap" IS NOT NULL
    ORDER BY "Market Cap" DESC
    LIMIT 10;
""").show()


# print("\n--- 5. SECTOR VALUATION & PROFITABILITY METRICS ---")
# con.sql("""
#     SELECT 
#         Sector,
#         COUNT(*) as company_count,
#         ROUND(AVG("Market Cap"), 0) as avg_market_cap,
#         ROUND(AVG("Earnings/Share"), 2) as avg_eps,
#         ROUND(MEDIAN("Price/Earnings"), 2) as median_pe
#     FROM sp500_company_data
#     WHERE "Market Cap" IS NOT NULL
#     GROUP BY Sector
#     ORDER BY avg_market_cap DESC;
# """).show()

# Always close the file lock handle when finished
con.close()