select
    case
        when distance_m < 250  then '0-250 m'
        when distance_m < 500  then '250-500 m'
        when distance_m < 1000 then '500-1000 m'
        when distance_m < 2000 then '1-2 km'
        else '2 km+'
    end as distance_band,
    case
        when distance_m < 250  then 1
        when distance_m < 500  then 2
        when distance_m < 1000 then 3
        when distance_m < 2000 then 4
        else 5
    end as band_order,
    least(station_zone_min, 6) as station_zone,
    room_type,
    count(*) as n_listings,
    round((percentile_cont(0.5) within group (order by price))::numeric, 2) as median_price,
    round((percentile_cont(0.5) within group (order by price / nullif(accommodates, 0)))::numeric, 2) as median_price_per_guest
from {{ ref('listings_with_distance') }}
group by 1, 2, 3, 4