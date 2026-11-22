import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine("postgresql+psycopg2://airbnb:airbnb@localhost:5432/airbnb")

df = pd.read_csv("data/raw/listings.csv.gz", dtype=str)
print(f"Read {len(df):,} rows, {len(df.columns)} columns")

with engine.begin() as conn:
    conn.execute(text("create schema if not exists raw"))

df.to_sql("listings", engine, schema="raw", if_exists="replace",
          index=False, chunksize=2000, method="multi")

with engine.connect() as conn:
    n = conn.execute(text("select count(*) from raw.listings")).scalar()
print(f"raw.listings now has {n:,} rows")
