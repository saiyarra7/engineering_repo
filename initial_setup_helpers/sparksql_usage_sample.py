from pyspark.sql import SparkSession

# 1. Initialize Spark Session
spark = SparkSession.builder \
    .appName("Biotech_LargeScale_Analysis") \
    .getOrCreate()

# 2. Load the massive datasets (Assume Parquet format for performance)
spark.read.parquet("s3://biotech-data/raw_sensors/").createOrReplaceTempView("sensor_readings")
spark.read.parquet("s3://biotech-data/metadata/").createOrReplaceTempView("experiments")

# 3. Use Spark SQL for the heavy lifting
# This query involves Filtering, Grouping, Aggregating, and Joining 10.5TB of data.
result = spark.sql("""
    WITH filtered_experiments AS (
        SELECT 
            experiment_id, 
            study_name,
            DATEDIFF(end_date, start_date) as duration_days
        FROM experiments
        WHERE status = 'COMPLETED'
    ),
    stats AS (
        SELECT 
            experiment_id,
            AVG(reading_value) as avg_value,
            STDDEV(reading_value) as stddev_value,
            COUNT(*) as reading_count
        FROM sensor_readings
        GROUP BY experiment_id
        HAVING COUNT(*) > 1000
    )
    SELECT 
        e.study_name,
        e.duration_days,
        s.avg_value,
        s.stddev_value
    FROM filtered_experiments e
    JOIN stats s ON e.experiment_id = s.experiment_id
    WHERE e.duration_days > 1
""")

# 4. Write the result (much smaller) back to S3
result.write.mode("overwrite").parquet("s3://biotech-data/results/experiment_stats/")