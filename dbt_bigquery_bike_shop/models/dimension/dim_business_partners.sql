select
    -- ids
    partner_id,
    address_id,
    created_by as employee_id,

    -- dimension
    company_name,
    partner_role,
    email_address,
    phone_number,
    fax_number,
    web_address,
    legal_form,
    currency,

    -- dates
    created_at
    
from {{ ref('stg_business_partners') }}