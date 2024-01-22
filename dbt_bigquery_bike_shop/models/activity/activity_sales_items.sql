with
sales_order_items as (
    select
        sales_order_id,
        sales_order_item_id,
        product_id,
        currency,
        gross_amount,
        net_amount,
        tax_amount,
        quantity,
        delivery_date
    from {{ ref('stg_sales_order_items') }}
),

sales_order as (
    select
        sales_order_id,
        created_at as sales_order_date,
        partner_id,
        case
            when billing_status = 'C' then 'Completed'
            when billing_status = 'I' then 'Incomplete'
            else 'Unknown'
        end as billing_status,
        case
            when delivery_status = 'C' then 'Completed'
            when delivery_status = 'I' then 'Incomplete'
            else 'Unknown'
        end as delivery_status
    from {{ ref('stg_sales_orders') }}
)

select
    -- ids
    soi.sales_order_id,
    soi.sales_order_item_id,
    soi.product_id,
    so.partner_id,

    -- date
    so.sales_order_date,
    soi.delivery_date,

    -- dimensions
    so.billing_status,
    so.delivery_status,
    soi.currency,

    -- metrics
    soi.gross_amount,
    soi.net_amount,
    soi.tax_amount,
    soi.quantity,
    soi.quantity * soi.gross_amount as total_gross_amount,
    soi.quantity * soi.net_amount as total_net_amount,
    soi.quantity * soi.tax_amount as total_tax_amount
from sales_order_items soi
left join sales_order so on soi.sales_order_id = so.sales_order_id
