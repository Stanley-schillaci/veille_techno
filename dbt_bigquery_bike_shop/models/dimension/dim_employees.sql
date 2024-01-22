select
    -- ids
    employee_id,
    address_id,

    -- dimension
    concat(name_first, ' ', name_last) as employee_name,
    case
        when sex = 'M' then 'Male'
        when sex = 'F' then 'Female'
        else 'Other'
    end as sex,
    case 
        when language = 'E' then 'English'
        when language = 'S' then 'Spanish'
        when language = 'F' then 'French'
        when language = 'C' then 'Chinese'
        else 'Other'
    end as language,
    phone_number,
    email_address,
    login_name
    
from {{ ref('stg_employees') }}
