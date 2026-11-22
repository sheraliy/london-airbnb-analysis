select
    c.listing_id,
    c.price,
    c.room_type,
    c.borough,
    c.latitude,
    c.longitude,
    c.number_of_reviews,
    c.review_scores_rating,
    c.accommodates,
    d.nearest_station,
    d.station_zone,
    split_part(d.station_zone, ' ', 1)::int as station_zone_min,
    d.distance_m
from {{ ref('clean_listings') }} c
join {{ source('raw', 'listing_nearest_station') }} d
    on c.listing_id = d.listing_id