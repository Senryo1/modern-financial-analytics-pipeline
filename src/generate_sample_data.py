"""
generate_sample_data.py

This script generates simulated financial and microfinance datasets
for the Modern Financial Analytics Pipeline project.

Generated files:
- customers.csv
- branches.csv
- advisors.csv
- products.csv
- loans.csv
- payments.csv

Output folder:
- data/raw/
"""

from pathlib import Path
from datetime import datetime, timedelta
import random
import pandas as pd


# -------------------------------------------------------------------
# Project paths
# -------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

random.seed(42)

NUM_CUSTOMERS = 20
NUM_LOANS = 40
NUM_PAYMENTS = 120


# -------------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------------

def random_date(start_date: datetime, end_date: datetime) -> datetime:
    """Return a random date between two dates."""
    delta_days = (end_date - start_date).days
    random_days = random.randint(0, delta_days)
    return start_date + timedelta(days=random_days)


def save_csv(df: pd.DataFrame, filename: str) -> None:
    """Save a DataFrame to the raw data folder."""
    output_path = RAW_DATA_DIR / filename
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Created: {output_path}")


# -------------------------------------------------------------------
# Generate branches
# -------------------------------------------------------------------

def generate_branches() -> pd.DataFrame:
    branches = [
        {"branch_id": "B001", "branch_name": "Central Branch", "region": "Metropolitan", "city": "Guatemala City"},
        {"branch_id": "B002", "branch_name": "Mixco Branch", "region": "Metropolitan", "city": "Mixco"},
        {"branch_id": "B003", "branch_name": "Villa Nueva Branch", "region": "Metropolitan", "city": "Villa Nueva"},
        {"branch_id": "B004", "branch_name": "Antigua Branch", "region": "Central", "city": "Antigua Guatemala"},
        {"branch_id": "B005", "branch_name": "Quetzaltenango Branch", "region": "Western", "city": "Quetzaltenango"},
    ]

    return pd.DataFrame(branches)


# -------------------------------------------------------------------
# Generate advisors
# -------------------------------------------------------------------

def generate_advisors(branches: pd.DataFrame) -> pd.DataFrame:
    advisor_names = [
        "Laura Ramirez",
        "Jose Morales",
        "Andrea Castillo",
        "Mario Lopez",
        "Sofia Hernandez",
        "Carlos Estrada",
        "Paola Garcia",
        "Daniel Perez",
    ]

    advisors = []

    for index, name in enumerate(advisor_names, start=1):
        branch_id = random.choice(branches["branch_id"].tolist())
        hire_date = random_date(datetime(2018, 1, 1), datetime(2023, 12, 31))

        advisors.append({
            "advisor_id": f"A{index:03d}",
            "advisor_name": name,
            "branch_id": branch_id,
            "hire_date": hire_date.date().isoformat(),
        })

    return pd.DataFrame(advisors)


# -------------------------------------------------------------------
# Generate products
# -------------------------------------------------------------------

def generate_products() -> pd.DataFrame:
    products = [
        {"product_id": "P001", "product_name": "Microloan Working Capital", "product_type": "Loan", "interest_rate": 0.18},
        {"product_id": "P002", "product_name": "Small Business Loan", "product_type": "Loan", "interest_rate": 0.15},
        {"product_id": "P003", "product_name": "Consumer Loan", "product_type": "Loan", "interest_rate": 0.22},
        {"product_id": "P004", "product_name": "Agricultural Loan", "product_type": "Loan", "interest_rate": 0.16},
        {"product_id": "P005", "product_name": "Women Entrepreneur Loan", "product_type": "Loan", "interest_rate": 0.14},
    ]

    return pd.DataFrame(products)


# -------------------------------------------------------------------
# Generate customers
# -------------------------------------------------------------------

def generate_customers() -> pd.DataFrame:
    first_names = [
        "Ana", "Carlos", "Maria", "Luis", "Sofia", "Jorge", "Elena", "Pedro",
        "Lucia", "Miguel", "Gabriela", "Fernando", "Diana", "Roberto", "Paola",
        "Andres", "Claudia", "Manuel", "Valeria", "Ricardo"
    ]

    last_names = [
        "Lopez", "Mendez", "Garcia", "Hernandez", "Ramirez", "Morales",
        "Castillo", "Perez", "Gomez", "Diaz", "Vasquez", "Rojas",
        "Flores", "Ortiz", "Alvarez", "Santos", "Reyes", "Cruz"
    ]

    cities = [
        "Guatemala City", "Mixco", "Villa Nueva", "Antigua Guatemala",
        "Quetzaltenango", "Escuintla", "Chimaltenango"
    ]

    segments = ["Individual", "Small Business", "Microenterprise"]
    genders = ["F", "M"]

    customers = []

    for index in range(1, NUM_CUSTOMERS + 1):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        gender = random.choice(genders)

        birth_date = random_date(datetime(1970, 1, 1), datetime(2003, 12, 31))
        registration_date = random_date(datetime(2019, 1, 1), datetime(2024, 12, 31))

        customers.append({
            "customer_id": f"C{index:03d}",
            "customer_name": f"{first_name} {last_name}",
            "gender": gender,
            "birth_date": birth_date.date().isoformat(),
            "registration_date": registration_date.date().isoformat(),
            "city": random.choice(cities),
            "customer_segment": random.choice(segments),
        })

    return pd.DataFrame(customers)


# -------------------------------------------------------------------
# Generate loans
# -------------------------------------------------------------------

def generate_loans(
    customers: pd.DataFrame,
    branches: pd.DataFrame,
    advisors: pd.DataFrame,
    products: pd.DataFrame
) -> pd.DataFrame:
    loan_statuses = ["Active", "Closed", "Delinquent"]
    loan_terms = [6, 12, 18, 24, 36]

    loans = []

    for index in range(1, NUM_LOANS + 1):
        customer_id = random.choice(customers["customer_id"].tolist())
        product_id = random.choice(products["product_id"].tolist())
        branch_id = random.choice(branches["branch_id"].tolist())

        advisors_in_branch = advisors[advisors["branch_id"] == branch_id]

        if advisors_in_branch.empty:
            advisor_id = random.choice(advisors["advisor_id"].tolist())
        else:
            advisor_id = random.choice(advisors_in_branch["advisor_id"].tolist())

        disbursement_date = random_date(datetime(2023, 1, 1), datetime(2025, 12, 31))

        loan_amount = random.choice([
            5000, 8000, 10000, 12000, 15000, 20000,
            25000, 30000, 45000, 60000
        ])

        loan_term_months = random.choice(loan_terms)
        loan_status = random.choices(
            loan_statuses,
            weights=[0.65, 0.25, 0.10],
            k=1
        )[0]

        loans.append({
            "loan_id": f"L{index:03d}",
            "customer_id": customer_id,
            "product_id": product_id,
            "branch_id": branch_id,
            "advisor_id": advisor_id,
            "disbursement_date": disbursement_date.date().isoformat(),
            "loan_amount": loan_amount,
            "loan_term_months": loan_term_months,
            "loan_status": loan_status,
        })

    return pd.DataFrame(loans)


# -------------------------------------------------------------------
# Generate payments
# -------------------------------------------------------------------

def generate_payments(loans: pd.DataFrame) -> pd.DataFrame:
    payments = []
    payment_statuses = ["Paid", "Late", "Missed"]

    for index in range(1, NUM_PAYMENTS + 1):
        selected_loan = loans.sample(1).iloc[0]

        loan_id = selected_loan["loan_id"]
        disbursement_date = datetime.strptime(selected_loan["disbursement_date"], "%Y-%m-%d")
        loan_amount = selected_loan["loan_amount"]
        loan_term_months = selected_loan["loan_term_months"]

        monthly_payment = round(loan_amount / loan_term_months, 2)

        payment_date = disbursement_date + timedelta(days=random.randint(30, 900))

        payment_status = random.choices(
            payment_statuses,
            weights=[0.75, 0.20, 0.05],
            k=1
        )[0]

        if payment_status == "Paid":
            days_late = 0
        elif payment_status == "Late":
            days_late = random.randint(1, 60)
        else:
            days_late = random.randint(61, 120)

        payment_amount = 0 if payment_status == "Missed" else monthly_payment

        payments.append({
            "payment_id": f"PMT{index:04d}",
            "loan_id": loan_id,
            "payment_date": payment_date.date().isoformat(),
            "payment_amount": payment_amount,
            "payment_status": payment_status,
            "days_late": days_late,
        })

    return pd.DataFrame(payments)


# -------------------------------------------------------------------
# Main execution
# -------------------------------------------------------------------

def main() -> None:
    print("Generating sample financial datasets...")

    branches = generate_branches()
    advisors = generate_advisors(branches)
    products = generate_products()
    customers = generate_customers()
    loans = generate_loans(customers, branches, advisors, products)
    payments = generate_payments(loans)

    save_csv(branches, "branches.csv")
    save_csv(advisors, "advisors.csv")
    save_csv(products, "products.csv")
    save_csv(customers, "customers.csv")
    save_csv(loans, "loans.csv")
    save_csv(payments, "payments.csv")

    print("Sample data generation completed successfully.")


if __name__ == "__main__":
    main()
