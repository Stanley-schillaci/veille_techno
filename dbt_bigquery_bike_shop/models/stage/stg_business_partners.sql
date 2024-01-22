select
    partnerid as partner_id,
    partnerrole as partner_role,
    emailaddress as email_address,
    phonenumber as phone_number,
    faxnumber as fax_number,
    webaddress as web_address,
    addressid as address_id,
    companyname as company_name,
    legalform as legal_form,
    createdby as created_by,
    parse_date('%Y%m%d', cast(createdat as string)) as created_at,
    changedby as changed_by,
    parse_date('%Y%m%d', cast(changedat as string)) as changed_at,
    currency
from RAW_CLIENT_BIKE_SHOP.business_partners