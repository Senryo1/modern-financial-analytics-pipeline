"""
run_sqlite_analytics.py

This script runs selected SQLite analytics queries against the local
financial_analytics.db database and exports the results to CSV files.

Input database:
- data/database/financial_analytics.db

Output folder:
- data/analytics/

Purpose:
This creates dashboard-ready analytical outputs from the local database layer.
"""

from pathlib import Path
import sqlite3
import pandas as pd


# -------------------------------------------------------------------
# Project paths
# -------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]
DATABASE_PATH = BASE_DIR / "data" / "database" / "financial_analytics.db"
ANALYTICS_OUTPUT_DIR = BASE_DIR / "data" / "analytics"

ANALYTICS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# -------------------------------------------------------------------
# Query definitions
# -------------------------------------------------------------------

ANALYTICS_QUERIES = {
    "executive_portfolio_kpis": """
        SELECT
            COUNT(*) AS total_loans,
            SUM(loan_amount) AS total_disbursed_amount,
            AVG(loan_amount) AS average_loan_amount,
            MIN(loan_amount) AS minimum_loan_amount,
            MAX(loan_amount) AS maximum_loan_amount
        FROM loans;
    """,

    "loan_portfolio_by_status": """
        SELECT
            loan_status,
            COUNT(*) AS loan_count,
            SUM(loan_amount) AS total_loan_amount,
            AVG(loan_amount) AS average_loan_amount
        FROM loans
        GROUP BY loan_status
        ORDER BY total_loan_amount DESC;
    """,

    "payment_status_distribution": """
        SELECT
            payment_status,
            COUNT(*) AS payment_count,
            SUM(payment_amount) AS total_payment_amount,
            AVG(days_late) AS average_days_late
        FROM payments
        GROUP BY payment_status
        ORDER BY payment_count DESC;
    """,

    "branch_performance": """
        SELECT
            b.branch_id,
            b.branch_name,
            b.region,
            b.city,
            COUNT(l.loan_id) AS loan_count,
            COALESCE(SUM(l.loan_amount), 0) AS total_loan_amount,
            AVG(l.loan_amount) AS average_loan_amount
        FROM branches b
        LEFT JOIN loans l
            ON b.branch_id = l.branch_id
        GROUP BY
            b.branch_id,
            b.branch_name,
            b.region,
            b.city
        ORDER BY total_loan_amount DESC;
    """,

    "advisor_performance": """
        SELECT
            a.advisor_id,
            a.advisor_name,
            b.branch_name,
            COUNT(l.loan_id) AS loan_count,
            COALESCE(SUM(l.loan_amount), 0) AS total_loan_amount,
            AVG(l.loan_amount) AS average_loan_amount
        FROM advisors a
        LEFT JOIN branches b
            ON a.branch_id = b.branch_id
        LEFT JOIN loans l
            ON a.advisor_id = l.advisor_id
        GROUP BY
            a.advisor_id,
            a.advisor_name,
            b.branch_name
        ORDER BY total_loan_amount DESC;
    """,

    "product_performance": """
        SELECT
            p.product_id,
            p.product_name,
            p.product_type,
            p.interest_rate,
            COUNT(l.loan_id) AS loan_count,
            COALESCE(SUM(l.loan_amount), 0) AS total_loan_amount,
            AVG(l.loan_amount) AS average_loan_amount
        FROM products p
        LEFT JOIN loans l
            ON p.product_id = l.product_id
        GROUP BY
            p.product_id,
            p.product_name,
            p.product_type,
            p.interest_rate
        ORDER BY total_loan_amount DESC;
    """,

    "customer_segment_analysis": """
        SELECT
            c.customer_segment,
            COUNT(DISTINCT c.customer_id) AS customer_count,
            COUNT(l.loan_id) AS loan_count,
            COALESCE(SUM(l.loan_amount), 0) AS total_loan_amount,
            AVG(l.loan_amount) AS average_loan_amount
        FROM customers c
        LEFT JOIN loans l
            ON c.customer_id = l.customer_id
        GROUP BY c.customer_segment
        ORDER BY total_loan_amount DESC;
    """,

    "monthly_payment_trend": """
        SELECT
            strftime('%Y-%m-01', payment_date) AS payment_month,
            COUNT(payment_id) AS payment_count,
            SUM(payment_amount) AS total_payment_amount,
            AVG(payment_amount) AS average_payment_amount,
            AVG(days_late) AS average_days_late
        FROM payments
        GROUP BY strftime('%Y-%m-01', payment_date)
        ORDER BY payment_month;
    """,

    "loan_level_analytics": """
        SELECT
            l.loan_id,
            l.customer_id,
            c.customer_name,
            c.customer_segment,
            c.city AS customer_city,
            l.product_id,
            p.product_name,
            p.interest_rate,
            l.branch_id,
            b.branch_name,
            b.region,
            l.advisor_id,
            a.advisor_name,
            l.disbursement_date,
            l.loan_amount,
            l.loan_term_months,
            l.loan_status,
            COUNT(pay.payment_id) AS payment_count,
            COALESCE(SUM(pay.payment_amount), 0) AS total_paid_amount,
            AVG(pay.days_late) AS average_days_late,
            SUM(
                CASE
                    WHEN pay.payment_status = 'Late' THEN 1
                    ELSE 0
                END
            ) AS late_payment_count,
            SUM(
                CASE
                    WHEN pay.payment_status = 'Missed' THEN 1
                    ELSE 0
                END
            ) AS missed_payment_count
        FROM loans l
        LEFT JOIN customers c
            ON l.customer_id = c.customer_id
        LEFT JOIN products p
            ON l.product_id = p.product_id
        LEFT JOIN branches b
            ON l.branch_id = b.branch_id
        LEFT JOIN advisors a
            ON l.advisor_id = a.advisor_id
        LEFT JOIN payments pay
            ON l.loan_id = pay.loan_id
        GROUP BY
            l.loan_id,
            l.customer_id,
            c.customer_name,
            c.customer_segment,
            c.city,
            l.product_id,
            p.product_name,
            p.interest_rate,
            l.branch_id,
            b.branch_name,
            b.region,
            l.advisor_id,
            a.advisor_name,
            l.disbursement_date,
            l.loan_amount,
            l.loan_term_months,
            l.loan_status;
    """,
}


# -------------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------------

def validate_database_exists() -> None:
    """Ensure the SQLite database exists before running analytics queries."""
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DATABASE_PATH}. "
            "Run src/load_to_sqlite.py before running analytics queries."
        )


def run_query_to_csv(
    connection: sqlite3.Connection,
    query_name: str,
    query: str
) -> None:
    """Run a SQL query and export the result to a CSV file."""
    output_path = ANALYTICS_OUTPUT_DIR / f"{query_name}.csv"

    df = pd.read_sql_query(query, connection)
    df.to_csv(output_path, index=False, encoding="utf-8")

    print(f"Created analytics output: {output_path} ({len(df)} rows)")


# -------------------------------------------------------------------
# Main process
# -------------------------------------------------------------------

def main() -> None:
    print("Starting SQLite analytics process...")

    validate_database_exists()

    with sqlite3.connect(DATABASE_PATH) as connection:
        for query_name, query in ANALYTICS_QUERIES.items():
            run_query_to_csv(connection, query_name, query)

    print("\nSQLite analytics process completed successfully.")


if __name__ == "__main__":
    main()