from pathlib import Path
import logging
import duckdb


# CONFIGURATION SETUP
TARGET_DIR = Path(r"C:\Users\Sai Yarra\Documents\tech_projects 2026\data")
DB_PATH = TARGET_DIR / "news_articles.duckdb"
ARTICLE_FILE = Path(r"C:\Users\Sai Yarra\Documents\tech_projects 2026\data\obesity_article.txt")
LOG_FILE = TARGET_DIR / "pipeline.log"

# Ensure directories exist before setting up the file logger
TARGET_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
)


def load_article_text(article_path: Path) -> str:
    """Reads the article body content from a text file."""
    logging.info(f"Reading article content from: {article_path}")
    if not article_path.exists():
        raise FileNotFoundError(f"Article file not found: {article_path}")
    return article_path.read_text(encoding="utf-8")


def load_article_to_warehouse(article_text: str, db_file: Path) -> None:
    """Creates the articles table and inserts a single article row into DuckDB."""
    logging.info("Preparing to write article row into DuckDB...")
    con = None
    try:
        con = duckdb.connect(database=str(db_file))
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS articles (
                article_id INTEGER,
                title TEXT,
                company TEXT,
                published_date DATE,
                body TEXT
            )
            """
        )
        con.execute(
            """
            INSERT INTO articles (article_id, title, company, published_date, body)
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                1,
                "GLP-1 Obesity Drug Market Intensifies",
                "Multiple",
                "2026-07-29",
                article_text,
            ],
        )
        logging.info("Article row successfully inserted into the articles table.")
    except Exception as e:
        logging.error(f"Article insertion failed: {str(e)}")
        raise
    finally:
        if con:
            con.close()


if __name__ == "__main__":
    logging.info("Starting article ingestion pipeline.")
    try:
        article_text = load_article_text(ARTICLE_FILE)
        load_article_to_warehouse(article_text, DB_PATH)
        logging.info("Pipeline completed successfully.")
    except Exception as pipeline_error:
        logging.critical(
            f"Pipeline terminated prematurely due to critical failure: {str(pipeline_error)}"
        )