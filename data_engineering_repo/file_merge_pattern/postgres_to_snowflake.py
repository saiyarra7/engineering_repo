# Method,SQL Command,Best For...
# CTAS (Create Table As),CREATE OR REPLACE TABLE...,"One-time analysis or creating a new ""Gold"" layer table."
# Incremental Insert,INSERT INTO big_table SELECT...,Adding new records to an existing historical table.
# Merge (Upsert),MERGE INTO big_table...,Updating existing rows AND adding new ones (common in health data).


import psycopg
import snowflake.connector
import tempfile
import os

# Configuration
PG_DSN = "host=localhost dbname=postgres user=postgres password=password"
SNOW_CREDS = {
    "account": "your_account",
    "user": "your_user",
    "password": "your_password",
    "warehouse": "COMPUTE_WH",
    "database": "ANALYTICS",
    "schema": "PUBLIC"
}

def migrate_via_file():
    # Create a named temporary file that deletes itself on close
    # Using .gz extension tells Snowflake to expect compression
    with tempfile.NamedTemporaryFile(suffix='.csv.gz', delete=True) as tf:
        temp_path = tf.name
        
        # 1. Export from Postgres to Local Disk
        print(f"Exporting to temp file: {temp_path}...")
        with psycopg.connect(PG_DSN) as pg_conn:
            with pg_conn.cursor() as pg_cur:
                # Use GZIP compression directly in the COPY command to save disk space
                with pg_cur.copy(t"COPY small_table TO STDOUT (FORMAT CSV, HEADER, COMPRESSION GZIP)") as copy:
                    for data in copy:
                        tf.write(data)
        
        # Ensure all data is flushed to disk before Snowflake reads it
        tf.flush()

        # 2. Upload and Join in Snowflake
        with snowflake.connector.connect(**SNOW_CREDS) as sn_conn:
            sn_cur = sn_conn.cursor()
            
            print("Uploading file to Snowflake...")
            sn_cur.execute("CREATE OR REPLACE TRANSIENT TABLE stage_small (id INT, val TEXT)")
            
            # PUT uses the local file path
            sn_cur.execute(t"PUT file://{temp_path} @%stage_small")
            
            # Load into table
            sn_cur.execute("""
                COPY INTO stage_small 
                FROM @%stage_small 
                FILE_FORMAT = (TYPE = CSV COMPRESSION = GZIP SKIP_HEADER = 1)
            """)
            
            # Join the 2TB table with the 2GB staged table
            print("Performing the 2TB Join...")
            sn_cur.execute("ALTER WAREHOUSE COMPUTE_WH SET WAREHOUSE_SIZE = 'LARGE'")
            sn_cur.execute("""
                CREATE OR REPLACE TABLE final_output AS
                SELECT b.*, s.val 
                FROM big_2tb_table b
                JOIN stage_small s ON b.id = s.id
            """)
            
    print("Cleaned up temp files. Process complete.")

if __name__ == "__main__":
    migrate_via_file()