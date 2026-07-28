import polars as pl
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# 1. GENERATE SAMPLE DATA (Clean & Structured)
np.random.seed(42)
num_rows = 1000

data = {
    "timestamp": [datetime(2026, 1, 1) + timedelta(hours=i) for i in range(num_rows)],
    "sample_id": [f"BATCH_{i%10:03d}" for i in range(num_rows)],
    "protein_concentration": np.random.normal(50, 10, num_rows),
    "p_value": np.random.uniform(0, 0.1, num_rows),
    "yield_score": np.random.uniform(0.7, 0.99, num_rows)
}

df = pl.DataFrame(data)

# 2. LOGICAL ANALYSIS
# Filtering for "significant" results and calculating rolling averages
analyzed_df = (
    df.lazy()
    .filter(pl.col("p_value") < 0.05)
    .with_columns([
        pl.col("protein_concentration").rolling_mean(window_size=5).alias("smooth_conc")
    ])
    .collect()
)

# 4. DATA INSPECTION (Run this before fig.show())

# Option A: The "Table" View - Optimized for width
# This ensures you see all columns and the first 20 rows clearly
with pl.Config(tbl_rows=20, tbl_width_chars=120, fmt_str_lengths=20):
    print("--- Eager DataFrame (Raw Data) ---")
    print(df.head(10))
    
    print("\n--- Analyzed DataFrame (Post-Filter & Smooth) ---")
    print(analyzed_df.head(10))

# Option B: The "Glimpse" View - Best for checking data types and values
# This lists columns vertically, which is better if your screen is narrow
print("\n--- Vertical Data Glimpse ---")
print(analyzed_df.glimpse())


# 3. HIGH-END VISUALIZATION
# This will open in the VS Code 'Interactive Window' or a browser tab
fig = px.line(
    analyzed_df.to_pandas(), 
    x="timestamp", 
    y="smooth_conc", 
    color="sample_id",
    title="Biotech Batch Yield Analysis (Synthetic)",
    template="plotly_dark"  # Looks better on a ThinkPad screen
)

fig.show()

# 4. PRINT PREVIEW (The clean way)
print("Data Summary:")
print(analyzed_df.head())