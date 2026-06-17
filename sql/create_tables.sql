DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS loans;

CREATE TABLE loans (
    loan_id INTEGER PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    loan_amount NUMERIC(12,2) NOT NULL,
    interest_rate NUMERIC(5,2) NOT NULL,
    term_months INTEGER NOT NULL,
    loan_status VARCHAR(20) NOT NULL,
    created_date DATE NOT NULL
);

CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY,
    loan_id INTEGER NOT NULL,
    amount NUMERIC(12,2) NOT NULL,
    payment_date DATE NOT NULL,

    CONSTRAINT fk_payment_loan
        FOREIGN KEY (loan_id)
        REFERENCES loans(loan_id)
);