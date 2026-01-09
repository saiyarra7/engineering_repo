import pandas as pd
import polars as pl
import numpy as np

# 1. GENERATE SAMPLE DATA (100k rows for a fair test)
data = {
    "id": np.arange(100_000),
    "category": np.random.choice(["A", "B", "C"], 100_000),
    "price": np.random.uniform(10, 500, 100_000),
    "qty": np.random.randint(1, 50, 100_000),
    "date": pd.date_range("2024-01-01", periods=100_000, freq="min")
}

# --- PANDAS WORKFLOW (Legacy/Eager) ---
df_pd = pd.DataFrame(data)

# --- POLARS WORKFLOW (Modern/Lazy) ---
df_pl = pl.DataFrame(data)

# ---------------------------------------------------------
# TASK 1: FILTERING & COLUMN CREATION
# ---------------------------------------------------------

# PANDAS: Imperative style (Step-by-step modification)
# We use .assign() to keep it somewhat clean, but it's single-threaded.
res_pd = df_pd[df_pd["category"] == "A"].assign(
    total_val = lambda x: x["price"] * x["qty"]
)

# POLARS: Declarative Expression style
# This is multi-threaded. .with_columns is the engine room of Polars.
res_pl = df_pl.filter(pl.col("category") == "A").with_columns(
    (pl.col("price") * pl.col("qty")).alias("total_val")
)

# ---------------------------------------------------------
# TASK 2: AGGREGATIONS (The "Bread and Butter")
# ---------------------------------------------------------

# PANDAS: Dictionary-based agg
agg_pd = df_pd.groupby("category").agg({
    "price": "mean",
    "qty": "sum"
}).reset_index()

# POLARS: List-based agg (Allows multiple operations on same column easily)
agg_pl = df_pl.group_by("category").agg([
    pl.col("price").mean().alias("avg_price"),
    pl.col("qty").sum().alias("total_qty")
])

# ---------------------------------------------------------
# TASK 3: CONDITIONAL LOGIC (If/Then/Else)
# ---------------------------------------------------------

# PANDAS: Usually requires np.where or a slow .apply()
df_pd["status"] = np.where(df_pd["price"] > 250, "Expensive", "Cheap")

# POLARS: Native 'when/then/otherwise' (Blazingly fast Rust implementation)
df_pl = df_pl.with_columns(
    pl.when(pl.col("price") > 250)
    .then(pl.lit("Expensive"))
    .otherwise(pl.lit("Cheap"))
    .alias("status")
)

# ---------------------------------------------------------
# TASK 4: TIME SERIES / WINDOW FUNCTIONS
# ---------------------------------------------------------

# PANDAS: Moving average
df_pd["rolling_avg"] = df_pd.groupby("category")["price"].transform(lambda x: x.rolling(5).mean())

# POLARS: Over() expressions (similar to SQL Window Functions)
df_pl = df_pl.with_columns(
    pl.col("price").mean().over("category").alias("cat_avg_price")
)

# ---------------------------------------------------------
# TASK 5: CONVERSION (The "Bridge")
# ---------------------------------------------------------

# Use Polars for the heavy lifting, then convert to Pandas for plotting/ML
final_df = df_pl.to_pandas()