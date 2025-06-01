import pandas as pd

file_path = "data/raw/train_delays.csv"

df = pd.read_csv(file_path, header=0)


print("Cleaned data:")
print(df.head())
print(f"Colums: {df.columns}")
print(f"Number of columns: {len(df.columns)}")

print("Final cleaned data:")
print(df.head())
print("Columns:", df.columns)
