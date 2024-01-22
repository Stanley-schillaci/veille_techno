with
sales_order as (
    select
        sales_order_id,
        created_at,
        created_by,
        fiscal_variant,
        partner_id,
        sales_org,
        gross_amount as order_gross_amount,
        net_amount as order_net_amount,
        tax_amount as order_tax_amount,
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
),

sales_order_item as (
    select
        sales_order_id,
        any_value(delivery_date) as delivery_date
    from {{ ref('stg_sales_order_items') }}
    group by sales_order_id
)

select
    -- ids
    so.sales_order_id,
    so.partner_id,
    so.created_by as employee_id,

    -- dates
    so.created_at as sales_order_date,
    soi.delivery_date,

    -- dimensions
    so.billing_status,
    so.delivery_status,
    so.sales_org,
    so.fiscal_variant,

    -- metrics
    so.order_gross_amount,
    so.order_net_amount,
    so.order_tax_amount
from sales_order so
left join sales_order_item soi
    on so.sales_order_id = soi.sales_order_id