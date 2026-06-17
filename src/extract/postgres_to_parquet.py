from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd
import os

# Load environment variables
load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")

# Database connection
engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

print("Connected to PostgreSQL")

# Extract loans
print("Extracting loans table...")

loans = pd.read_sql(
    "SELECT * FROM loans",
    engine
)

loans.to_parquet(
    "data/processed/loans.parquet",
    index=False
)

print(f"Exported {len(loans)} loans")

# Extract payments
print("Extracting payments table...")

payments = pd.read_sql(
    "SELECT * FROM payments",
    engine
)

payments.to_parquet(
    "data/processed/payments.parquet",
    index=False
)

print(f"Exported {len(payments)} payments")

print("Parquet extraction complete")