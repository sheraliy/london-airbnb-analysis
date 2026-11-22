select
    listing_id,
    price,
    room_type,
    borough,
    latitude,
    longitude,
    number_of_reviews,
    review_scores_rating,
    accommodates
from {{ ref('stg_listings') }}
where price between 10 and 1000
  and latitude is not null
  and longitude is not null