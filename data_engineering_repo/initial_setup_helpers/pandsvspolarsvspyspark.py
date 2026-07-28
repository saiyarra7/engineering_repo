import pandas as pd

# Data is processed immediately and stored in RAM
df = pd.DataFrame({
    "id": [1, 2, 3, 4],
    "category": ["A", "B", "A", "B"],
    "value": [100, 200, 150, 300]
})

# Transformations are immediate (eager)
df["taxed_value"] = df["value"] * 1.1
result = df[df["value"] > 120].groupby("category")["taxed_value"].mean()

print(result)


##------------------------------------------------------------------------------

import polars as pl

# 1. Scan data lazily (doesn't load into RAM yet)
# Using pl.LazyFrame or .scan_csv() / .scan_parquet()
df = pl.DataFrame({
    "id": [1, 2, 3, 4],
    "category": ["A", "B", "A", "B"],
    "value": [100, 200, 150, 300]
}).lazy()

# 2. Define the Query Plan
query = (
    df.with_columns((pl.col("value") * 1.1).alias("taxed_value"))
    .filter(pl.col("value") > 120)
    .group_by("category")
    .agg(pl.col("taxed_value").mean())
)

# 3. Execute (collect() triggers the Rust-backed engine)
print(query.collect())

##------------------------------------------------------------------------------

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("Comparison").getOrCreate()

# 1. Create Distributed DataFrame
data = [(1, "A", 100), (2, "B", 200), (3, "A", 150), (4, "B", 300)]
df = spark.createDataFrame(data, ["id", "category", "value"])

# 2. Define Transformations (Lazy - only metadata is updated)
result_df = df.withColumn("taxed_value", col("value") * 1.1) \
              .filter(col("value") > 120) \
              .groupBy("category") \
              .avg("taxed_value")

# 3. Trigger Action (Compute across the cluster)
result_df.show()