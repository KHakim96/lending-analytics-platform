from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import pandas as pd
import os
import json

# Load environment variables
load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")

# Create database connection
engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

print("Connected to PostgreSQL")

# --------------------------------------------------
# Reset tables during development
# --------------------------------------------------

with engine.begin() as conn:
    conn.execute(text("TRUNCATE TABLE payments;"))
    conn.execute(text("TRUNCATE TABLE loans;"))

print("Tables truncated")

# --------------------------------------------------
# Load Loans
# --------------------------------------------------

print("Loading loans.csv...")

loans = pd.read_csv("data/loans.csv")

# Remove duplicate loan IDs
loans = loans.drop_duplicates(subset=["loan_id"])

def safe_json_parse(value):
    try:
        return json.loads(value) if pd.notna(value) else None
    except Exception:
        return None

# Convert borrower_info to JSON string
loans["borrower_info"] = loans["borrower_info"].apply(
    lambda x: json.dumps(safe_json_parse(x))
    if pd.notna(x)
    else None
)

loans.to_sql(
    "loans",
    engine,
    if_exists="append",
    index=False,
    method="multi"
)

print(f"Loaded {len(loans)} loans")

# --------------------------------------------------
# Load Payments
# --------------------------------------------------

print("Loading payments.jsonl...")

payments = pd.read_json(
    "data/payments.jsonl",
    lines=True
)

# Remove duplicate payment IDs
payments = payments.drop_duplicates(subset=["payment_id"])

# Convert JSON columns to strings
payments["payment_method"] = payments["payment_method"].apply(
    lambda x: json.dumps(x) if pd.notna(x) else None
)

payments["metadata"] = payments["metadata"].apply(
    lambda x: json.dumps(x) if pd.notna(x) else None
)

payments.to_sql(
    "payments",
    engine,
    if_exists="append",
    index=False,
    method="multi"
)

print(f"Loaded {len(payments)} payments")

print("Seed load complete")