select

    loan_id,
    customer_id,

    lower(trim(product_type)) as product_type,

    try_to_number(
        replace(
            replace(principal_amount, '$', ''),
            ',', ''
        ),
        38,
        2
    ) as principal_amount,

    interest_rate,

    term_months,

    coalesce(
        try_to_date(origination_date, 'YYYY-MM-DD'),
        try_to_date(origination_date, 'DD-MON-YYYY'),
        try_to_date(origination_date, 'MM/DD/YYYY')
    ) as origination_date,

    lower(trim(origination_channel)) as origination_channel,

    lower(trim(status)) as status,

    borrower_info

from RAW.LOANS