select
    -- ids
    address_id,
    
    -- dimension
    city,
    postal_code,
    street,
    building,
    country,
    region,
    address_type,
    latitude,
    longitude
    
from {{ ref('stg_adresses') }}