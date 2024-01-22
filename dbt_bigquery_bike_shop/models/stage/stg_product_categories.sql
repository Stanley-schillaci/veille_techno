select
    prodcategoryid as product_category_id,
    createdby as created_by,
    parse_date('%Y%m%d', cast(createdat as string)) as created_at
from RAW_CLIENT_BIKE_SHOP.product_categories