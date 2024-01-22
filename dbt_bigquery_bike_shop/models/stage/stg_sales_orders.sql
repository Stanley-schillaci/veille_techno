select
    salesorderid as sales_order_id,
    createdby as created_by,
    parse_date('%Y%m%d', cast(createdat as string)) as created_at,
    changedby as changed_by,
    parse_date('%Y%m%d', cast(changedat as string)) as changed_at,
    fiscvariant as fiscal_variant,
    fiscalyearperiod as fiscal_year_period,
    noteid as note_id,
    partnerid as partner_id,
    salesorg as sales_org,
    currency as currency,
    grossamount as gross_amount,
    netamount as net_amount,
    taxamount as tax_amount,
    lifecyclestatus as lifecycle_status,
    billingstatus as billing_status,
    deliverystatus as delivery_status
from RAW_CLIENT_BIKE_SHOP.sales_orders