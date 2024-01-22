select
    addressid as address_id,
    city,
    postalcode as postal_code,
    street,
    building,
    country,
    region,
    addresstype as address_type,
    parse_date('%Y%m%d', cast(validity_startdate as string)) AS validity_start_date,
    parse_date('%Y%m%d', cast(validity_enddate as string)) AS validity_end_date,
    latitude,
    longitude
from RAW_CLIENT_BIKE_SHOP.adresses