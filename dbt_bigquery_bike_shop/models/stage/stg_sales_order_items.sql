select
    salesorderid as sales_order_id,
    salesorderitem as sales_order_item,
    concat(salesorderid, salesorderitem) as sales_order_item_id,
    productid as product_id,
    noteid as note_id,
    currency,
    grossamount as gross_amount,
    netamount as net_amount,
    taxamount as tax_amount,
    itematpstatus as item_atp_status,
    opitempos as op_item_pos,
    quantity,
    quantityunit as quantity_unit,
    parse_date('%Y%m%d', cast(deliverydate as string)) as delivery_date
from RAW_CLIENT_BIKE_SHOP.sales_order_items