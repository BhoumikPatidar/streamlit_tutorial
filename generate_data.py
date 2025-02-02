import pandas as pd
import numpy as np

# Generate 100 rows of random data
data = {
    "date": pd.date_range(start="2024-01-01", periods=100),
    "sales": np.random.randint(50, 200, 100),
    "revenue": np.random.normal(5000, 1500, 100).round(2),
    "product_id": np.random.choice(["A", "B", "C"], 100),
    "customer_rating": np.random.uniform(1, 5, 100).round(1)
}

df = pd.DataFrame(data)
df.to_csv("sample_data.csv", index=False)