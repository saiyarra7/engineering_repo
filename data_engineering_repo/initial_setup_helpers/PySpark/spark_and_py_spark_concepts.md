# Apache Spark & PySpark — Interview‑Focused Jupyter Notebook

## One‑sentence summary
This notebook systematically covers Apache Spark and PySpark concepts most frequently tested in data engineering interviews, with concise explanations and executable code examples.

---

## 0. Setup Assumptions
```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql import Window

spark = (
    SparkSession.builder
    .appName("spark-interview-notebook")
    .master("local[*]")
    .getOrCreate()
)
```

---

## 1. Spark Architecture (Interview Critical)

### Key Components
1. **Driver**: Orchestrates execution, holds DAG, runs SparkContext
2. **Cluster Manager**: Allocates resources (YARN, Kubernetes, Standalone)
3. **Executors**: Run tasks, store data in memory/disk
4. **Tasks**: Smallest unit of execution
5. **Jobs → Stages → Tasks**: Execution hierarchy

**Interview trap**: Spark is *not* a database; it is a distributed compute engine.

---

## 2. RDDs (Low‑level, still asked)

### Create RDD
```python
rdd = spark.sparkContext.parallelize([1, 2, 3, 4, 5])
```

### Transformations vs Actions
```python
rdd2 = rdd.map(lambda x: x * 2)   # transformation
result = rdd2.collect()          # action
```

### Narrow vs Wide Transformations
```python
rdd.map(lambda x: (x, 1))         # narrow
rdd.groupBy(lambda x: x % 2)      # wide (shuffle)
```

**Interview rule**: Wide transformations trigger shuffles.

---

## 3. DataFrames and Spark SQL (Most Important)

### Create DataFrame
```python
data = [(1, "A", 100), (2, "B", 200), (3, "A", 300)]
df = spark.createDataFrame(data, ["id", "category", "value"])
df.show()
```

### Select, Filter
```python
df.select("id", "value").filter(F.col("value") > 150)
```

### Column Expressions
```python
df.withColumn("value_plus_10", F.col("value") + 10)
```

---

## 4. Lazy Evaluation

```python
filtered = df.filter(F.col("value") > 100)  # no execution yet
filtered.count()                             # triggers execution
```

**Interview question**: Why is Spark lazy?
- Enables query optimization
- Reduces unnecessary computation

---

## 5. DAG, Jobs, Stages

```python
df.groupBy("category").agg(F.sum("value")).explain(True)
```

**Key idea**:
- Action → Job
- Shuffle boundary → Stage split

---

## 6. Joins (Very High Frequency)

### Join Types
```python
df1 = spark.createDataFrame([(1, "A"), (2, "B")], ["id", "left_val"])
df2 = spark.createDataFrame([(1, "X"), (3, "Y")], ["id", "right_val"])

# Inner
df1.join(df2, "id", "inner")

# Left
df1.join(df2, "id", "left")
```

### Broadcast Join
```python
from pyspark.sql.functions import broadcast

df1.join(broadcast(df2), "id")
```

**Interview rule**: Broadcast when one side < ~10–100MB.

---

## 7. Aggregations & GroupBy

```python
df.groupBy("category").agg(
    F.count("id").alias("cnt"),
    F.sum("value").alias("total")
)
```

---

## 8. Window Functions (Mandatory for Senior Roles)

```python
window_spec = Window.partitionBy("category").orderBy(F.col("value").desc())

df.withColumn("rank", F.rank().over(window_spec))
```

Common functions:
- row_number
- rank / dense_rank
- lead / lag

---

## 9. Handling Nulls

```python
df.fillna({"value": 0})
df.dropna()
```

---

## 10. UDFs (And Why to Avoid Them)

```python
from pyspark.sql.types import IntegerType

@F.udf(IntegerType())
def square(x):
    return x * x

df.withColumn("squared", square(F.col("value")))
```

**Interview rule**:
- Prefer Spark SQL functions over UDFs (Catalyst cannot optimize UDFs).

---

## 11. Caching and Persistence

```python
df.cache()
df.persist()
df.unpersist()
```

Storage levels:
- MEMORY_ONLY
- MEMORY_AND_DISK

---

## 12. Partitioning & Repartitioning

```python
df.rdd.getNumPartitions()

df.repartition(10)
df.coalesce(2)
```

**Interview rule**:
- repartition → shuffle
- coalesce → avoids shuffle

---

## 13. File Formats (Common Questions)

```python
df.write.mode("overwrite").parquet("/tmp/data")
```

Comparison:
- **Parquet**: columnar, compressed, splittable
- **ORC**: similar, strong Hive support
- **CSV/JSON**: slow, schema inference cost

---

## 14. Schema Management

```python
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("category", StringType(), True)
])

spark.createDataFrame(data=[(1, "A")], schema=schema)
```

**Interview rule**: Always provide schema in production.

---

## 15. Performance Tuning (Very High Frequency)

### Key Levers
1. Avoid shuffles
2. Use broadcast joins
3. Control partitions
4. Use column pruning & predicate pushdown
5. Cache only reused datasets

```python
spark.conf.set("spark.sql.shuffle.partitions", 200)
```

---

## 16. Catalyst Optimizer & Tungsten

- **Catalyst**: Logical + physical plan optimization
- **Tungsten**: Binary memory format, whole‑stage codegen

**Interview answer**: Spark is fast due to Catalyst + Tungsten.

---

## 17. Fault Tolerance & Lineage

```python
rdd.toDebugString()
```

Spark recomputes lost partitions using lineage, not replication.

---

## 18. Checkpointing

```python
spark.sparkContext.setCheckpointDir("/tmp/checkpoints")
df.checkpoint()
```

Used to truncate long lineage chains.

---

## 19. Skew Handling

Techniques:
1. Broadcast joins
2. Salting keys
3. AQE (Adaptive Query Execution)

```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
```

---

## 20. AQE (Frequently Asked in 2024–2026)

AQE can:
- Change join strategies at runtime
- Coalesce shuffle partitions
- Handle skew dynamically

---

## 21. Structured Streaming (Interview Basics)

```python
stream_df = (
    spark.readStream
    .format("rate")
    .load()
)
```

Concepts:
- Micro‑batch model
- Exactly‑once semantics
- Watermarking

---

## 22. Common Interview Traps

1. `collect()` on large data → OOM
2. Too many small files
3. Over‑caching
4. UDF abuse
5. Ignoring data skew

---

## 23. Typical Interview Questions to Practice

1. Difference between repartition and coalesce
2. When does Spark shuffle
3. How Spark handles failures
4. Broadcast join vs shuffle join
5. Why Parquet is faster than CSV

---

## 24. Final Mental Model

Spark = Lazy + Distributed + Optimized SQL Engine

If you can explain **why** Spark does something, not just **how**, you pass senior interviews.

---

End of notebook.

