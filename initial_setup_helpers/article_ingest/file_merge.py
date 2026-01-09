import pandas as pd

# 1. Setup Mock Data (Reproduceable Example)
df_left = pd.DataFrame({
    'user_id': [1, 2, 3, 4],
    'name': ['Alice', 'Bob', 'Charlie', 'David'],
    'region': ['FL', 'TX', 'NY', 'FL']
})

df_right = pd.DataFrame({
    'user_id': [3, 4, 5, 6],
    'last_login': ['2025-10-01', '2025-10-15', '2025-10-20', '2025-10-22'],
    'score': [85, 92, 78, 88]
})

# 2. Inner Join: Intersection of keys (Only 3 and 4)
inner = pd.merge(df_left, df_right, on='user_id', how='inner')

# 3. Left Join: Keep all from df_left (1, 2, 3, 4). 1 and 2 will have NaNs for right columns.
left = pd.merge(df_left, df_right, on='user_id', how='left')

# 4. Outer Join: Union of all keys (1, 2, 3, 4, 5, 6). Maximum data retention.
outer = pd.merge(df_left, df_right, on='user_id', how='outer')

# 5. Handling Different Column Names
df_other = df_right.rename(columns={'user_id': 'id_num'})
diff_names = pd.merge(df_left, df_other, left_on='user_id', right_on='id_num')

# Print results to console for verification
print("--- Inner Join ---\n", inner)
print("\n--- Left Join ---\n", left)