from decimal import Decimal

import pandas as pd
from google.cloud import bigquery
from sqlalchemy import create_engine

PROJECT = "london-airbnb-bek-01"
DATASET = "london_airbnb"
TABLES = ["price_by_borough", "price_by_distance_band", "price_quality_ratio"]

pg = create_engine("postgresql+psycopg2://airbnb:airbnb@localhost:5432/airbnb")
bq = bigquery.Client(project=PROJECT)

for name in TABLES:
    df = pd.read_sql(f"select * from analytics_gold.{name}", pg)
    for col in df.select_dtypes(include="object").columns:
        if df[col].map(lambda v: isinstance(v, Decimal)).any():
            df[col] = df[col].astype(float)
    job = bq.load_table_from_dataframe(
        df,
        f"{PROJECT}.{DATASET}.{name}",
        job_config=bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE"),
    )
    job.result()
    print(f"{name}: {len(df)} rows loaded")