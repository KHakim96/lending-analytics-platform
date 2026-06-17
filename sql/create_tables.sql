DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS loans;

CREATE TABLE loans (
    loan_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20),
    product_type VARCHAR(50),
    principal_amount TEXT,
    interest_rate NUMERIC(10,2),
    term_months INTEGER,
    origination_date TEXT,
    origination_channel VARCHAR(50),
    status VARCHAR(50),
    borrower_info JSONB
);



CREATE TABLE payments (
    payment_id VARCHAR(20) PRIMARY KEY,
    loan_id VARCHAR(20),
    amount NUMERIC(12,2),
    timestamp TEXT,
    payment_method JSONB,
    metadata JSONB
);