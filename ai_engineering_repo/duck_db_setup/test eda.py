import duckdb
from pathlib import Path

DB_PATH = Path(r"C:\Users\Sai Yarra\Documents\tech_projects 2026\data\sp500_company_data.duckdb")

with duckdb.connect(str(DB_PATH)) as con:
    # 1) Quick schema check
    con.sql("DESCRIBE sp500_company_data").show()

    # 2) Quick summary without loading the whole table
    overview = con.sql("""
        SELECT
            COUNT(*) AS total_rows,
            COUNT(DISTINCT Symbol) AS unique_companies,
            COUNT(DISTINCT Sector) AS unique_sectors
        FROM sp500_company_data
    """).df()

    print(overview)

    # 3) Preview a small sample
    sample = con.sql("""
        SELECT *
        FROM sp500_company_data
        LIMIT 10
    """).df()

    print(sample)

    # 4) EDA summary in SQL
    sector_summary = con.sql("""
        SELECT
            Sector,
            COUNT(*) AS company_count,
            ROUND(AVG("Market Cap"), 0) AS avg_market_cap,
            ROUND(AVG("Earnings/Share"), 2) AS avg_eps,
            ROUND(MEDIAN("Price/Earnings"), 2) AS median_pe
        FROM sp500_company_data
        WHERE "Market Cap" IS NOT NULL
        GROUP BY Sector
        ORDER BY avg_market_cap DESC
    """).df()

    print(sector_summary)

    # 5) Top companies by market cap
    top_caps = con.sql("""
        SELECT
            Symbol,
            Name,
            Sector,
            "Market Cap",
            "Price/Earnings" AS PE_Ratio
        FROM sp500_company_data
        WHERE "Market Cap" IS NOT NULL
        ORDER BY "Market Cap" DESC
        LIMIT 10
    """).df()

    print(top_caps)