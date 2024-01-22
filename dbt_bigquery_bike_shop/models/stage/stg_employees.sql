select
    employeeid as employee_id,
    name_first, 
    name_middle, 
    name_last, 
    name_initials,
    sex,
    language,
    phonenumber as phone_number,
    emailaddress as email_address,
    loginname as login_name,
    addressid as address_id,
    parse_date('%Y%m%d', cast(validity_startdate as string)) as validity_start_date,
    parse_date('%Y%m%d', cast(validity_enddate as string)) as validity_end_date
from RAW_CLIENT_BIKE_SHOP.employees