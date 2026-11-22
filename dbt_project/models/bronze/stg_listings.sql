select
    id::bigint                                                            as listing_id,
    nullif(replace(replace(price, '$', ''), ',', ''), '')::numeric(10,2)  as price,
    room_type,
    neighbourhood_cleansed                                                as borough,
    latitude::double precision                                            as latitude,
    longitude::double precision                                           as longitude,
    number_of_reviews::int                                                as number_of_reviews,
    review_scores_rating::numeric(3,2)                                    as review_scores_rating,
    nullif(accommodates, '')::int                                         as accommodates
from {{ source('raw', 'listings') }}