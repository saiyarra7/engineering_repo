import polars as pl
from datetime import date

# 1. Setup sample data (Simulating your Activity table)
data = {
    "player_id": [1, 1, 1, 2, 2],
    "event_date": [
        date(2026, 1, 1), date(2026, 1, 2), date(2026, 1, 5), # Player 1: Retained
        date(2026, 1, 1), date(2026, 1, 5)                   # Player 2: Not Retained
    ]
}
df = pl.DataFrame(data).lazy() # Use LazyFrame for performance

# 2. Initialize the SQL Context and register the dataframe
# 'register_entities=True' automatically finds dataframes in your local scope
ctx = pl.SQLContext(register_entities=True)

# 3. Define the SQL Query (Using the Postgres-style logic we discussed)
# Note: Polars SQL supports standard SQL syntax including CTEs
query = """
WITH player_stats AS (
    SELECT 
        player_id, 
        MIN(event_date) OVER(PARTITION BY player_id) as first_day,
        event_date
    FROM df
)
SELECT 
    ROUND(
        COUNT(DISTINCT CASE 
            WHEN event_date = first_day + INTERVAL '1 day' THEN player_id 
        END) * 1.0 / COUNT(DISTINCT player_id), 
        2
    ) AS fraction
FROM player_stats
"""

# 4. Execute and Collect
# .execute() creates the plan, .collect() runs the computation
result = ctx.execute(query).collect()

print(result)