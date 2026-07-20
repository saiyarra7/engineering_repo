import polars as pl

# Database connection credentials
# In production, these should be environment variables
DB_CONFIG = {
    "user": "analyst_admin",
    "password": "secure_password",
    "host": "rds-clinical-01.aws.com",
    "port": "5432",
    "dbname": "patient_data"
}

def get_postgres_data(query: str) -> pl.DataFrame:
    """
    Connects to Postgres and returns data as a Polars DataFrame.
    Uses 'connectorx' for high-speed, zero-copy data transfer.
    """
    
    # 1. Create the Connection URI
    # Format: postgresql://username:password@host:port/database
    uri = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"

    # 2. Fetch the data
    # 'connectorx' engine is significantly faster than standard drivers
    # It utilizes your Ryzen's multi-threading to pull data in parallel
    df = pl.read_database_uri(query=query, uri=uri, engine="connectorx")
    
    return df

# --- How to use it ---

# Define your SQL query (Vectorized filters are faster in the DB side)
sql = "SELECT patient_id, blood_pressure, heart_rate FROM clinical_trials WHERE age > 18"

# Get the data
try:
    clinical_df = get_postgres_data(sql)
    
    # Simple Polars transformation
    print(f"Fetched {len(clinical_df)} rows.")
    print(clinical_df.head())
    
except Exception as e:
    print(f"Error connecting to database: {e}")