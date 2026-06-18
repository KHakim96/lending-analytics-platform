select

    payment_id,
    loan_id,
    amount,
    timestamp

from {{ ref('stg_payments') }}