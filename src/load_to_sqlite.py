"""
load_to_sqlite.py

This script loads processed financial datasets into a local SQLite database.

Input folder:
- data/processed/

Output database:
- data/database/financial_analytics.db

Purpose:
This creates a lightweight database layer so SQL analytics and data quality
logic can be tested against relational tables.
"""

from pathlib import Path
import sqlite3
import pandas as pd


# -------------------------------------------------------------------
# Project paths
# -------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
DATABASE_DIR = BASE_DIR / "data" / "database"
DATABASE_PATH = DATABASE_DIR / "financial_analytics.db"

DATABASE_DIR.mkdir(parents=True, exist_ok=True)


# -------------------------------------------------------------------
# Dataset configuration
# -------------------------------------------------------------------

DATASETS = {
    "customers": "customers_processed.csv",
    "branches": "branches_processed.csv",
    "advisors": "advisors_processed.csv",
    "products": "products_processed.csv",
    "loans": "loans_processed.csv",
    "payments": "payments_processed.csv",
}


# -------------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------------

def read_processed_dataset(filename: str) -> pd.DataFrame:
    """Read a processed CSV file from data/processed/."""
    file_path = PROCESSED_DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"Processed file not found: {file_path}. "
            "Run src/transform.py before loading data to SQLite."
        )

    return pd.read_csv(file_path)


def load_dataframe_to_sqlite(
    df: pd.DataFrame,
    table_name: str,
    connection: sqlite3.Connection
) -> None:
    """
    Load a DataFrame into SQLite.

    if_exists='replace' makes the load idempotent for local development:
    running the script multiple times recreates the tables with the latest
    processed data.
    """
    df.to_sql(
        name=table_name,
        con=connection,
        if_exists="replace",
        index=False
    )

    print(f"Loaded table: {table_name} ({len(df)} rows)")


def create_indexes(connection: sqlite3.Connection) -> None:
    """
    Create basic indexes for frequently joined fields.

    These indexes are not strictly necessary for the small sample dataset,
    but they document the intended relational access patterns.
    """
    index_statements = [
        "CREATE INDEX IF NOT EXISTS idx_loans_customer_id ON loans(customer_id);",
        "CREATE INDEX IF NOT EXISTS idx_loans_product_id ON loans(product_id);",
        "CREATE INDEX IF NOT EXISTS idx_loans_branch_id ON loans(branch_id);",
        "CREATE INDEX IF NOT EXISTS idx_loans_advisor_id ON loans(advisor_id);",
        "CREATE INDEX IF NOT EXISTS idx_payments_loan_id ON payments(loan_id);",
        "CREATE INDEX IF NOT EXISTS idx_advisors_branch_id ON advisors(branch_id);",
    ]

    cursor = connection.cursor()

    for statement in index_statements:
        cursor.execute(statement)

    connection.commit()
    print("Indexes created successfully.")


def validate_loaded_tables(connection: sqlite3.Connection) -> None:
    """Print row counts for all loaded tables."""
    print("\nLoaded table row counts:")

    for table_name in DATASETS.keys():
        query = f"SELECT COUNT(*) AS row_count FROM {table_name};"
        row_count = pd.read_sql_query(query, connection).iloc[0]["row_count"]
        print(f"- {table_name}: {row_count} rows")


# -------------------------------------------------------------------
# Main process
# -------------------------------------------------------------------

def main() -> None:
    print("Starting SQLite load process...")
    print(f"Database path: {DATABASE_PATH}")

    with sqlite3.connect(DATABASE_PATH) as connection:
        for table_name, filename in DATASETS.items():
            df = read_processed_dataset(filename)
            load_dataframe_to_sqlite(df, table_name, connection)

        create_indexes(connection)
        validate_loaded_tables(connection)

    print("\nSQLite load process completed successfully.")


if __name__ == "__main__":
    main()