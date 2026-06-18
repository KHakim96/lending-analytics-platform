select distinct

    customer_id

from {{ ref('stg_loans') }}

where customer_id is not null