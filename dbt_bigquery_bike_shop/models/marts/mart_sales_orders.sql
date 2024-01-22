with
sales_order as (
    select
        sales_order_id,
        partner_id,
        employee_id,

        billing_status,
        delivery_status,
        case 
            when delivery_status = 'Completed' then delivery_date
            else null
        end as delivery_date,
        sales_order_date,

        order_gross_amount,
        order_net_amount,
        (order_gross_amount / order_net_amount) * 100 as order_tax_rate,

        case
            when billing_status = 'Completed' then order_gross_amount
            else 0
        end as billing_gross_amount,

        case
            when billing_status = 'Completed' then order_net_amount
            else 0
        end as billing_net_amount,

    from {{ ref('activity_sales_orders') }}
),

business_partner as (
    select
        partner_id,
        address_id,

        company_name,
        legal_form
    from {{ ref('dim_business_partners') }}
),

employee as (
    select
        employee_id,
        employee_name
    from {{ ref('dim_employees') }}
),

adresses as (
    select
        address_id,
        country,
        city
    from {{ ref('dim_adresses') }}
)

select
    so.sales_order_date,

    bp.company_name,
    bp.legal_form,
    a.country,
    a.city,

    e.employee_name,

    so.billing_status,
    so.delivery_status,
    so.delivery_date,

    so.order_gross_amount,
    so.order_net_amount,
    so.order_tax_rate,
    so.billing_gross_amount,
    so.billing_net_amount,
    so.sales_order_id as order_number
from sales_order so
left join business_partner bp on so.partner_id = bp.partner_id
left join adresses a on bp.address_id = a.address_id
left join employee e on so.employee_id = e.employee_id
order by so.sales_order_date
