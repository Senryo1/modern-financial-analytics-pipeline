
"""
transform.py

This script reads raw financial datasets from data/raw/,
applies basic cleaning and standardization rules, and saves
processed datasets into data/processed/.

Input folder:
- data/raw/

Output folder:
- data/processed/
"""

from pathlib import Path
import pandas as pd


# -------------------------------------------------------------------
# Project paths
# -------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)


# -------------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------------

def read_csv(filename: str) -> pd.DataFrame:
    """Read a CSV file from the raw data folder."""
    file_path = RAW_DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    return pd.read_csv(file_path)


def save_processed_csv(df: pd.DataFrame, filename: str) -> None:
    """Save a processed DataFrame to the processed data folder."""
    output_path = PROCESSED_DATA_DIR / filename
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Processed file created: {output_path}")


def clean_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Trim spaces in text columns."""
    df = df.copy()

    text_columns = df.select_dtypes(include=["object"]).columns

    for column in text_columns:
        df[column] = df[column].astype(str).str.strip()

    return df


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names to lowercase snake_case."""
    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    return df


def convert_date_columns(df: pd.DataFrame, date_columns: list[str]) -> pd.DataFrame:
    """Convert selected columns to datetime format."""
    df = df.copy()

    for column in date_columns:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column], errors="coerce")

    return df


def convert_numeric_columns(df: pd.DataFrame, numeric_columns: list[str]) -> pd.DataFrame:
    """Convert selected columns to numeric format."""
    df = df.copy()

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    return df


# -------------------------------------------------------------------
# Dataset-specific transformations
# -------------------------------------------------------------------

def transform_customers() -> pd.DataFrame:
    """Transform customers dataset."""
    df = read_csv("customers.csv")
    df = standardize_column_names(df)
    df = clean_text_columns(df)

    df = convert_date_columns(
        df,
        ["birth_date", "registration_date"]
    )

    return df


def transform_branches() -> pd.DataFrame:
    """Transform branches dataset."""
    df = read_csv("branches.csv")
    df = standardize_column_names(df)
    df = clean_text_columns(df)

    return df


def transform_advisors() -> pd.DataFrame:
    """Transform advisors dataset."""
    df = read_csv("advisors.csv")
    df = standardize_column_names(df)
    df = clean_text_columns(df)

    df = convert_date_columns(
        df,
        ["hire_date"]
    )

    return df


def transform_products() -> pd.DataFrame:
    """Transform products dataset."""
    df = read_csv("products.csv")
    df = standardize_column_names(df)
    df = clean_text_columns(df)

    df = convert_numeric_columns(
        df,
        ["interest_rate"]
    )

    return df


def transform_loans() -> pd.DataFrame:
    """Transform loans dataset."""
    df = read_csv("loans.csv")
    df = standardize_column_names(df)
    df = clean_text_columns(df)

    df = convert_date_columns(
        df,
        ["disbursement_date"]
    )

    df = convert_numeric_columns(
        df,
        ["loan_amount", "loan_term_months"]
    )

    return df


def transform_payments() -> pd.DataFrame:
    """Transform payments dataset."""
    df = read_csv("payments.csv")
    df = standardize_column_names(df)
    df = clean_text_columns(df)

    df = convert_date_columns(
        df,
        ["payment_date"]
    )

    df = convert_numeric_columns(
        df,
        ["payment_amount", "days_late"]
    )

    return df


# -------------------------------------------------------------------
# Main execution
# -------------------------------------------------------------------

def main() -> None:
    print("Starting data transformation process...")

    customers = transform_customers()
    branches = transform_branches()
    advisors = transform_advisors()
    products = transform_products()
    loans = transform_loans()
    payments = transform_payments()

    save_processed_csv(customers, "customers_processed.csv")
    save_processed_csv(branches, "branches_processed.csv")
    save_processed_csv(advisors, "advisors_processed.csv")
    save_processed_csv(products, "products_processed.csv")
    save_processed_csv(loans, "loans_processed.csv")
    save_processed_csv(payments, "payments_processed.csv")

    print("Data transformation process completed successfully.")


if __name__ == "__main__":
    main()
