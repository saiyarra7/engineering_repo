from pyspark.sql import SparkSession
from pyspark.sql import functions as F

def standardize_news():
    spark = SparkSession.builder.getOrCreate()

    # 1. Setup Auto Loader to ingest JSON files from S3
    # 'cloudFiles' is Databricks' optimized streaming source
    raw_path = "s3://amgen-raw-zone/news-ingestion/"
    checkpoint_path = "dbfs:/checkpoints/news_bronze_to_silver/"
    target_table = "catalog.news_db.silver_articles"

    raw_stream = (spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.schemaLocation", "dbfs:/schemas/news_raw")
        .load(raw_path))

    # 2. Standardize Schema using Spark SQL logic
    # We handle FactSet, Muckrack, and Factiva in one transformation
    standardized_df = raw_stream.select(
        F.col("article_id").cast("string").alias("id"),
        F.trim(F.col("headline")).alias("title"),
        F.to_timestamp(F.col("timestamp")).alias("event_time"),
        F.col("vendor_name").alias("source"),
        F.col("content").alias("raw_body"),
        F.current_timestamp().alias("ingested_at")
    ).filter("title IS NOT NULL")

    # 3. Write as a Delta Table (Silver Layer)
    query = (standardized_df.writeStream
        .format("delta")
        .outputMode("append")
        .option("checkpointLocation", checkpoint_path)
        .trigger(availableNow=True) # Runs as a batch-like stream for cost efficiency
        .toTable(target_table))
    
    query.awaitTermination()

if __name__ == "__main__":
    standardize_news()