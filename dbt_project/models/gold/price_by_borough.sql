select
    borough,
    room_type,
    count(*) as n_listings,
    round((percentile_cont(0.5) within group (order by price))::numeric, 2) as median_price,
    round(avg(price), 2) as avg_price
from {{ ref('listings_with_distance') }}
group by borough, room_type