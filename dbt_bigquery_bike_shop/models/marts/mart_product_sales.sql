with
sales_order_item as (
    select
        sales_order_item_id,
        product_id,
        partner_id,

        sales_order_date,

        billing_status,
        delivery_status,

        case 
            when delivery_status = 'Completed' then delivery_date
            else null
        end as delivery_date,

        (tax_amount / gross_amount) * 100 as tax_rate,

        quantity,
        total_gross_amount,
        total_net_amount,

        case 
            when billing_status = 'Completed' then total_gross_amount
            else 0
        end as billing_gross_amount,

        case 
            when billing_status = 'Completed' then total_net_amount
            else 0
        end as billing_net_amount

    from {{ ref('activity_sales_items') }}
),

product as (
    select
        product_id,
        product_category_id,
        product_description,
        category_description,
        price as product_price,
        weight_measure,
        weight_unit
    from {{ ref('dim_product') }}
),

partner as (
    select
        partner_id,
        company_name
    from {{ ref('dim_business_partners') }}
)

select
    soi.sales_order_date,

    p.product_id as product_name,
    p.product_description,
    p.product_category_id as category_name,
    p.category_description,

    par.company_name,

    soi.billing_status,
    soi.delivery_status,
    soi.delivery_date,

    soi.quantity,
    p.product_price,
    p.weight_measure,
    p.weight_unit,

    soi.total_gross_amount,
    soi.total_net_amount,
    soi.tax_rate,

    soi.billing_gross_amount,
    soi.billing_net_amount,

    soi.sales_order_item_id as order_number

from sales_order_item as soi
left join product as p on p.product_id = soi.product_id
left join partner as par on par.partner_id = soi.partner_id
order by sales_order_date


