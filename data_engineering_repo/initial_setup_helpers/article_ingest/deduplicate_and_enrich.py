from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql import functions as F

def process_gold_layer():
    spark = SparkSession.builder.getOrCreate()

    # 1. Load Silver Data
    silver_df = spark.read.table("catalog.news_db.silver_articles")

    # 2. Complex Deduplication (The "Spark Scenario")
    # We partition by title to find duplicates and rank by vendor quality
    window_spec = Window.partitionBy("title").orderBy(
        F.col("event_time").asc(), 
        F.expr("CASE WHEN source = 'FactSet' THEN 1 ELSE 2 END")
    )

    deduped_df = (silver_df
        .withColumn("rank", F.row_number().over(window_spec))
        .filter("rank = 1")
        .drop("rank"))

    # 3. Text Chunking for GenAI (Pre-processing)
    # Exploding long text into 2000-character chunks for LLM context windows
    def chunk_text(text):
        if not text: return []
        size = 2000
        return [text[i:i+size] for i in range(0, len(text), size)]

    chunk_udf = F.udf(chunk_text, "array<string>")

    enriched_df = (deduped_df
        .withColumn("chunks", chunk_udf(F.col("raw_body")))
        .withColumn("chunk_text", F.explode(F.col("chunks")))
        .select("id", "title", "source", "chunk_text"))

    # 4. Save to Gold for API/LLM consumption
    enriched_df.write \
        .format("delta") \
        .mode("overwrite") \
        .saveAsTable("catalog.news_db.gold_summarization_input")

if __name__ == "__main__":
    process_gold_layer()