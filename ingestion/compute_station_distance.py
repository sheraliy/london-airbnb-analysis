import numpy as np
import pandas as pd
from sklearn.neighbors import BallTree
from sqlalchemy import create_engine, text

EARTH_RADIUS_M = 6_371_000

engine = create_engine("postgresql+psycopg2://airbnb:airbnb@localhost:5432/airbnb")

stations = pd.read_csv(
    "data/reference/london_underground_metadata.csv", dtype={"zone": str}
)
stations = (
    stations[["station_name", "zone", "latitude", "longitude"]]
    .dropna(subset=["latitude", "longitude"])
    .reset_index(drop=True)
)
print(f"{len(stations)} station rows")
print("zone values:", sorted(stations["zone"].unique()))

with engine.connect() as conn:
    listings = pd.read_sql(
        text("""
            select id::bigint as listing_id,
                   latitude::double precision as latitude,
                   longitude::double precision as longitude
            from raw.listings
            where latitude is not null and longitude is not null
        """),
        conn,
    )
print(f"{len(listings):,} listings")

# BallTree + haversine: coordinates must be [lat, lon] in radians
tree = BallTree(
    np.radians(stations[["latitude", "longitude"]].to_numpy()), metric="haversine"
)
dist, idx = tree.query(
    np.radians(listings[["latitude", "longitude"]].to_numpy()), k=1
)

result = pd.DataFrame(
    {
        "listing_id": listings["listing_id"],
        "nearest_station": stations.loc[idx[:, 0], "station_name"].to_numpy(),
        "station_zone": stations.loc[idx[:, 0], "zone"].to_numpy(),
        "distance_m": (dist[:, 0] * EARTH_RADIUS_M).round(1),
    }
)

result.to_sql(
    "listing_nearest_station",
    engine,
    schema="raw",
    if_exists="replace",
    index=False,
    chunksize=5000,
    method="multi",
)

print(result["distance_m"].describe().round(1))