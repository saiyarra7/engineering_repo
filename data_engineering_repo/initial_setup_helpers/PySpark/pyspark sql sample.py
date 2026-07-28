# 1. Load data using PySpark
df = spark.read.parquet("s3://your-bucket/raw-data/")

# 2. Register as a SQL view
df.createOrReplaceTempView("raw_data")

# 3. Use your SQL skills (This runs in parallel across the cluster!)
enriched_df = spark.sql("""
    SELECT 
        user_id, 
        SUM(amount) as total_spend,
        ROW_NUMBER() OVER(PARTITION BY category ORDER BY date DESC) as rank
    FROM raw_data
    WHERE status = 'active'
    GROUP BY user_id, category, date
""")

# 4. Save the result
enriched_df.write.format("delta").mode("overwrite").saveAsTable("silver_layer.user_summary")