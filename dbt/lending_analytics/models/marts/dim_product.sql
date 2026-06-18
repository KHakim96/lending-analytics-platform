select distinct

    product_type

from {{ ref('stg_loans') }}

where product_type is not null