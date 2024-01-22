with
products as (
    select
        product_id,
        product_category_id,
        partner_id,
        type_code,
        currency,
        created_at,
        created_by,
        weight_measure,
        weight_unit,
        price,

    from {{ ref('stg_products') }}
),

product_text as (
    select
        product_id,
        any_value(short_description) as product_description
    from {{ ref('stg_product_texts') }}
    group by product_id
),

product_category as (
    select
        product_category_id,
        any_value(short_description) as category_description
    from {{ ref('stg_product_category_text') }}
    group by product_category_id
)

select 
    -- ids
    p.product_id,
    p.product_category_id,
    p.partner_id,
    p.created_by as employee_id,

    -- dimension
    pt.product_description,
    pc.category_description,
    p.type_code,
    p.currency,

    -- mesures / metrics
    p.weight_measure,
    p.weight_unit,
    p.price,

    -- date
    p.created_at

from products p
left join product_text pt on p.product_id = pt.product_id
left join product_category pc on p.product_category_id = pc.product_category_id
