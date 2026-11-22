# London Airbnb: Price, Distance to Tube and Borough

An end-to-end data pipeline (Python, PostgreSQL, dbt, BigQuery, Looker Studio) that asks:
**what drives Airbnb prices in London, distance to the nearest Tube station or the area?**

Dashboard (PDF, 4 pages): [docs/dashboard.pdf](docs/dashboard.pdf)

## Findings
- **Zone drives price more than distance.** Median price per guest (entire homes, 0-250 m
  from a Tube station): about £80 in Zone 1, £60 in Zone 2, £48 in Zone 3.
- **Within a zone, distance matters only beyond ~1 km.** Zone 1: £80 (0-250 m) to £65.7
  (1-2 km). Zone 2: £60.5 to £48.4 (2 km+). Within 500 m, differences are small and
  inconsistent in direction.
- **Borough medians** (entire homes with a listed price) range from £141.5 (Sutton) to
  £302 (Westminster); sample sizes range from 196 (Sutton) to 6,248 (Westminster).
- **Ratings barely differ between boroughs** (4.65-4.83, entire homes with 10+ reviews).
  No clear link between price and rating is visible; correlation was not computed.

## Data
- Inside Airbnb, London listings: 91,954 rows, 90 columns. Source: <https://insideairbnb.com/get-the-data/>
  (check the site's license before reuse).
- London Underground stations (272 rows, with fare zone): <https://zenodo.org/records/18313509>.

Neither file is stored in this repository.

## Pipeline
1. `ingestion/load_raw_to_postgres.py`: loads the CSV into `raw.listings` as text (no type
   changes, so raw stays an exact copy of the source).
2. `ingestion/compute_station_distance.py`: nearest Tube station per listing with
   scikit-learn `BallTree` (haversine metric). 91,954 listings x 272 stations.
3. dbt: **bronze** (types, renaming), **silver** (filters, join with distance),
   **gold** (aggregates by borough, zone and distance band).
4. `gcp/load_to_bigquery.py`: loads the gold tables to BigQuery; the dashboard is built in
   Looker Studio on top of them.

## Data quality
- 91,954 listings in source, 58,923 analysed. Dropped: 32,049 without a price, 982 priced
  above £1000 per night (outlier cap).
- dbt: 6 models, 9 tests (not null, unique, accepted values), all passing.
- The join with the distance table keeps all 58,923 rows.

## Limitations
- 34.9% of listings have no price, and the share varies by borough (17.8% to 50.7%). The
  cause was not established, so price results cover only listings that show a price.
- Distance is straight-line (haversine), not walking distance.
- Station data covers London Underground only (no Elizabeth line, Overground, DLR or rail),
  so distance to transport is overstated in areas such as Lewisham and Greenwich.
- Zone is the zone of the nearest station, a proxy for the listing's own zone.
- The scatter chart's Y axis is truncated (4.6-4.9), which visually exaggerates small
  rating differences.
- Descriptive analysis only: no confidence intervals and no causal claims.

## How to run
```bash
docker compose up -d
python ingestion/load_raw_to_postgres.py
python ingestion/compute_station_distance.py
cd dbt_project && dbt run && dbt test && cd ..
python gcp/load_to_bigquery.py   # set PROJECT in the script to your GCP project ID
```

Local Postgres credentials in `docker-compose.yml` and `dbt_project/profiles.yml`
(`airbnb`/`airbnb`) are for local development only.