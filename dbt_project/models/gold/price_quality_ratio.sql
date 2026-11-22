select
    borough,
    count(*) as n_listings,
    round((percentile_cont(0.5) within group (order by price))::numeric, 2) as median_price,
    round(avg(review_scores_rating), 3) as avg_rating,
    round(
        (percentile_cont(0.5) within group (order by price))::numeric
        / nullif(avg(review_scores_rating), 0), 2
    ) as price_per_rating_point
from {{ ref('listings_with_distance') }}
where room_type = 'Entire home/apt'
  and number_of_reviews >= 10
  and review_scores_rating is not null
group by borough