from pathlib import Path
import logging
import duckdb
import polars as pl


# CONFIGURATION SETUP
TARGET_DIR = Path(r"C:\Users\Sai Yarra\Documents\tech_projects 2026\data")
CSV_PATH = TARGET_DIR / "sp500_company_data_source.csv"
DB_PATH = TARGET_DIR / "sp500_company_data.duckdb"
LOG_FILE = TARGET_DIR / "pipeline.log"
DATA_URL = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies-financials/main/data/constituents-financials.csv"

# Ensure directories exist before setting up the file logger
TARGET_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
)

# PIPELINE FUNCTIONS

def extract_and_save_data(url: str, output_csv: Path) -> pl.DataFrame:
    """Streams data from the remote URL and saves a local CSV backup."""
    logging.info(f"Initiating download from source URL: {url}")
    try:
        df = pl.read_csv(url)
        logging.info(
            f"Successfully downloaded dataset. Shape: {df.shape[0]} rows, {df.shape[1]} columns."
        )

        df.write_csv(output_csv)
        logging.info(f"Raw source CSV backup successfully written to: {output_csv}")
        return df
    except Exception as e:
        logging.error(f"Failed to extract or back up raw data: {str(e)}")
        raise


def load_to_warehouse(df: pl.DataFrame, db_file: Path) -> None:
    """Initializes DuckDB storage and writes the Polars DataFrame to disk."""
    logging.info(f"Opening connection to local DuckDB file: {db_file}")
    con = None
    try:
        con = duckdb.connect(database=str(db_file))

        # Atomic structural operations inside DuckDB
        con.execute(
            "CREATE TABLE IF NOT EXISTS sp500_company_data AS SELECT * FROM df"
        )
        logging.info("Table 'sp500_company_data' successfully verified/written.")
    except Exception as e:
        logging.error(f"Database operation failed during table creation: {str(e)}")
        raise
    finally:
        if con:
            con.close()
            logging.info("DuckDB connection safely terminated.")


def run_analytics_query(db_file: Path) -> pl.DataFrame:
    """Executes the standard analytical aggregate query against the storage layer."""
    logging.info("Executing analytical aggregate query...")
    query = """
        SELECT 
            Sector,
            COUNT(*) as company_count,
            ROUND(AVG("Earnings/Share"), 2) as avg_eps,
            SUM(CAST("Market Cap" AS BIGINT)) as total_market_cap
        FROM sp500_company_data
        WHERE "Market Cap" IS NOT NULL
        GROUP BY Sector
        ORDER BY total_market_cap DESC;
    """
    con = None
    try:
        con = duckdb.connect(database=str(db_file))
        result = con.execute(query).pl()
        logging.info("Analytics query completed successfully.")
        return result
    except Exception as e:
        logging.error(f"Failed to execute analytical query: {str(e)}")
        raise
    finally:
        if con:
            con.close()



# Funcation calls

if __name__ == "__main__":
    logging.info("Starting S&P 500 fundamentals data engineering pipeline.")
    try:
        # Step 1: Extract and Backup
        raw_df = extract_and_save_data(DATA_URL, CSV_PATH)

        # Step 2: Load into Local Data Warehouse
        load_to_warehouse(raw_df, DB_PATH)

        # Step 3: Run Validation/Analytics
        summary_metrics = run_analytics_query(DB_PATH)

        # Print final result frame to standard out
        print("\n", summary_metrics)

        logging.info("Pipeline execution completed successfully.")

    except Exception as pipeline_error:
        logging.critical(
            f"Pipeline terminated prematurely due to critical failure: {str(pipeline_error)}"
        )