

# Data Engineering Strategy: Scaling Postgres (2GB) to Snowflake (2TB)

## 1. Executive Summary
This document outlines the high-performance ELT (Extract, Load, Transform) pattern for merging a 2GB relational dataset (Postgres) with a 2TB analytical warehouse (Snowflake). 

**Core Principle:** Move the small data to the large data. Avoid data egress from Snowflake at all costs.

---

## 2. Technical Implementation (Python 3.14 + Psycopg 3)

### Optimized Migration Script
This script uses **Binary Export** and **Local File Staging** to minimize RAM overhead and maximize throughput.

```python
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

def migrate_and_merge():
    # Use a temp file to handle 2GB safely regardless of Local RAM
    with tempfile.NamedTemporaryFile(suffix='.csv.gz', delete=True) as tf:
        
        # 1. High-Performance Binary Extract from Postgres
        print("Extracting from Postgres...")
        with psycopg.connect(PG_DSN) as pg_conn:
            with pg_conn.cursor() as pg_cur:
                # Compression happens during the copy to minimize disk I/O
                with pg_cur.copy("COPY small_table TO STDOUT (FORMAT CSV, HEADER, COMPRESSION GZIP)") as copy:
                    for data in copy:
                        tf.write(data)
        tf.flush()

        # 2. Snowflake Ingestion & Scaled Join
        with snowflake.connector.connect(**SNOW_CREDS) as sn_conn:
            sn_cur = sn_conn.cursor()
            
            # Use TRANSIENT to save on Fail-safe storage costs
            sn_cur.execute("CREATE OR REPLACE TRANSIENT TABLE stage_small (id INT, val TEXT)")
            
            # Upload to Snowflake Internal Stage
            sn_cur.execute(f"PUT file://{tf.name} @%stage_small")
            
            # Bulk Load
            sn_cur.execute("""
                COPY INTO stage_small 
                FROM @%stage_small 
                FILE_FORMAT = (TYPE = CSV COMPRESSION = GZIP SKIP_HEADER = 1)
            """)

            # 3. The Broadcast Join (Merge Pattern)
            # Scaling the warehouse to LARGE ensures 2GB fits in memory (No Disk Spilling)
            sn_cur.execute("ALTER WAREHOUSE COMPUTE_WH SET WAREHOUSE_SIZE = 'LARGE'")
            
            sn_cur.execute("""
                MERGE INTO big_2tb_table target
                USING stage_small source
                ON target.id = source.id
                WHEN MATCHED THEN
                    UPDATE SET target.metadata = source.val
                WHEN NOT MATCHED THEN
                    INSERT (id, metadata) VALUES (source.id, source.val);
            """)
            
    print("Pipeline Execution Successful.")

if __name__ == "__main__":
    migrate_and_merge()