select

    loan_id,
    customer_id,
    product_type,

    principal_amount,
    interest_rate,
    term_months,

    origination_date,
    origination_channel,

    status

from {{ ref('stg_loans') }}