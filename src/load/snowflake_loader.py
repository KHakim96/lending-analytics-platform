from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd
import os
import json


load_dotenv()

# Snowflake credentials
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")

# Create Snowflake connection
engine = create_engine(
    f"snowflake://{SNOWFLAKE_USER}:{SNOWFLAKE_PASSWORD}@{SNOWFLAKE_ACCOUNT}/"
    f"{SNOWFLAKE_DATABASE}/{SNOWFLAKE_SCHEMA}"
    f"?warehouse={SNOWFLAKE_WAREHOUSE}"
)

print("Connected to Snowflake")

# Load parquet files
print("Loading loans parquet...")

loans = pd.read_parquet(
    "data/processed/loans.parquet"
)

loans["borrower_info"] = loans["borrower_info"].apply(
    lambda x: json.dumps(x) if pd.notna(x) else None
)

loans.to_sql(
    name="LOANS",
    con=engine,
    schema="RAW",
    if_exists="append",
    index=False
)

print(f"Loaded {len(loans)} loans")

print("Loading payments parquet...")

payments = pd.read_parquet(
    "data/processed/payments.parquet"
)

payments["payment_method"] = payments["payment_method"].apply(
    lambda x: json.dumps(x) if pd.notna(x) else None
)

payments["metadata"] = payments["metadata"].apply(
    lambda x: json.dumps(x) if pd.notna(x) else None
)

payments.to_sql(
    name="PAYMENTS",
    con=engine,
    schema="RAW",
    if_exists="append",
    index=False
)

print(f"Loaded {len(payments)} payments")

print("Snowflake load complete")