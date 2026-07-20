from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[*]").getOrCreate()
print(f"Spark Version: {spark.version}")