# Modern Financial Analytics Pipeline

## Project Overview

This project demonstrates a modern data analytics pipeline for a financial or microfinance business scenario.

The goal is to transform raw operational data into clean, validated, analytics-ready datasets that can support executive reporting, portfolio monitoring, data quality checks, and business decision-making.

This project is designed as a professional portfolio project focused on:

- Data Engineering
- Analytics Engineering
- Data Quality
- Financial Analytics
- SQL Analytics
- Python-based data processing
- Technical documentation
- Business rule validation

---

## Business Context

Financial and microfinance institutions often manage customer, loan, payment, branch, advisor, and product data across different systems.

When this information is inconsistent, manually processed, or poorly documented, reporting becomes slow, unreliable, and difficult to scale.

This project simulates that scenario and builds a structured workflow to move data from raw operational files into validated, analytics-ready datasets.

---

## Project Objectives

The main objectives of this project are:

1. Generate realistic simulated financial datasets.
2. Organize data into raw, processed, and sample layers.
3. Clean and standardize datasets using Python.
4. Validate data quality using Python.
5. Document SQL-based data quality checks.
6. Build analytical SQL queries for reporting.
7. Document data architecture, business rules, and field definitions.
8. Prepare the foundation for a future Power BI dashboard, dbt project, and cloud data warehouse implementation.

---

## High-Level Architecture

```text
Sample Data Generation
        ↓
Raw Data Layer
        ↓
Python Transformation Layer
        ↓
Processed Data Layer
        ↓
Python Data Quality Validation
        ↓
SQL Data Quality Checks
        ↓
SQL Analytics Queries
        ↓
Power BI / Reporting Layer
        ↓
Technical Documentation
```

---

## Repository Structure

```text
modern-financial-analytics-pipeline/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
│
├── src/
│   ├── generate_sample_data.py
│   ├── extract.py
│   ├── transform.py
│   └── validate.py
│
├── sql/
│   ├── data_quality_checks.sql
│   └── analytics_queries.sql
│
├── docs/
│   ├── architecture.md
│   ├── data_dictionary.md
│   ├── business_rules.md
│   └── code_walkthrough.md
│
└── dashboards/
    └── powerbi/
```

---

## Data Model

The project simulates a simplified financial analytics data model.

| Dataset | Description |
|---|---|
| `customers` | Customer master data |
| `branches` | Branch or agency information |
| `advisors` | Credit advisor information |
| `products` | Financial product catalog |
| `loans` | Loan portfolio data |
| `payments` | Loan payment transaction data |

---

## Main Relationships

| Child Dataset | Child Field | Parent Dataset | Parent Field |
|---|---|---|---|
| `loans` | `customer_id` | `customers` | `customer_id` |
| `loans` | `product_id` | `products` | `product_id` |
| `loans` | `branch_id` | `branches` | `branch_id` |
| `loans` | `advisor_id` | `advisors` | `advisor_id` |
| `advisors` | `branch_id` | `branches` | `branch_id` |
| `payments` | `loan_id` | `loans` | `loan_id` |

---

## Current Pipeline Status

| Layer | Status |
|---|---|
| Repository setup | Completed |
| Sample data generation | Completed |
| Raw data layer | Completed |
| Sample data for portfolio review | Completed |
| Python transformation | Completed |
| Processed data layer | Completed |
| Python validation | Completed |
| SQL data quality checks | Completed |
| SQL analytics queries | Completed |
| Technical documentation | Completed |
| Power BI dashboard | Pending |
| dbt models | Future phase |
| Snowflake/cloud warehouse | Future phase |
| Airflow orchestration | Future phase |
| Docker environment | Future phase |

---

## Tools and Technologies

Current tools:

- Python
- pandas
- SQL
- Git
- GitHub
- Markdown
- Power BI planned

Future tools:

- dbt
- Snowflake or another cloud data warehouse
- Airflow
- Docker
- GitHub Actions

---

## Python Scripts

### `src/generate_sample_data.py`

Generates simulated financial and microfinance datasets.

Outputs:

```text
data/raw/customers.csv
data/raw/branches.csv
data/raw/advisors.csv
data/raw/products.csv
data/raw/loans.csv
data/raw/payments.csv
```

It also creates smaller visible sample files under:

```text
data/sample/
```

These sample files are included in GitHub so reviewers can inspect the data structure without running the full pipeline.

---

### `src/transform.py`

Reads raw datasets from:

```text
data/raw/
```

and writes cleaned datasets to:

```text
data/processed/
```

Main transformation logic:

- Standardizes column names.
- Trims text values.
- Converts date fields.
- Converts numeric fields.
- Saves processed datasets.

---

### `src/validate.py`

Runs Python-based data quality validations on processed datasets.

Validation categories:

- Missing values
- Duplicate primary keys
- Allowed categorical values
- Positive and non-negative numeric values
- Referential integrity
- Business rule consistency

Validation outputs:

```text
data/validation/validation_summary.csv
data/validation/validation_details.csv
```

The validation summary provides one row per validation check, including status, dataset name, failed record count, and description.

The validation details file stores failed records when validation issues are detected.

These outputs are generated locally and are not versioned in GitHub because they can be recreated by running the validation script.


---
### `src/load_to_sqlite.py`

Loads processed datasets into a local SQLite database.

Input:

```text
data/processed/
```

Output:

```text
data/database/financial_analytics.db
```

Purpose:

This script creates a lightweight local database layer so the processed datasets can be queried as relational tables.

Loaded tables:

- `customers`
- `branches`
- `advisors`
- `products`
- `loans`
- `payments`

The generated SQLite database is not versioned in GitHub because it can be recreated by running the pipeline.

---

### `src/run_sqlite_analytics.py`

Runs selected SQLite-compatible analytics queries against the local database and exports dashboard-ready CSV outputs.

Input:

```text
data/database/financial_analytics.db
```

Output:

```text
data/analytics/
```

Generated analytics outputs include:

- `executive_portfolio_kpis.csv`
- `loan_portfolio_by_status.csv`
- `payment_status_distribution.csv`
- `branch_performance.csv`
- `advisor_performance.csv`
- `product_performance.csv`
- `customer_segment_analysis.csv`
- `monthly_payment_trend.csv`
- `loan_level_analytics.csv`

These files are generated locally and are not versioned in GitHub because they can be recreated by running the analytics script.

## SQL Scripts

### `sql/data_quality_checks.sql`

Contains SQL-based data quality checks.

The logic is:

```text
If a query returns rows, those records should be reviewed.
If a query returns zero rows, the validation passes.
```

Validation areas:

- Primary key duplicates
- Critical null values
- Invalid numeric values
- Invalid categorical values
- Referential integrity
- Business rule violations
- Financial consistency checks

---

### `sql/analytics_queries.sql`

Contains analytical SQL queries for financial and microfinance reporting.

Analysis areas:

- Executive portfolio KPIs
- Loan portfolio by status
- Payment behavior
- Branch performance
- Advisor performance
- Product performance
- Customer segment analysis
- Monthly trends
- Recovery analysis
- Power BI-ready datasets

---

## Documentation

The project includes technical and business documentation under the `docs/` folder.

| Document | Purpose |
|---|---|
| `architecture.md` | Explains the project architecture and pipeline layers |
| `data_dictionary.md` | Describes datasets, fields, relationships, and analytical grain |
| `business_rules.md` | Documents data quality and business validation rules |
| `code_walkthrough.md` | Explains the logic and design decisions behind the code |

---

### 6. Load processed data into SQLite

```bash
python src/load_to_sqlite.py
```

or:

```bash
py src/load_to_sqlite.py
```

This creates a local SQLite database at:

```text
data/database/financial_analytics.db
```

---

### 7. Run SQLite analytics outputs

```bash
python src/run_sqlite_analytics.py
```

or:

```bash
py src/run_sqlite_analytics.py
```

This generates analytics-ready CSV outputs under:

```text
data/analytics/
```

## How to Run the Project

### 1. Clone the repository

```bash
git clone <repository-url>
cd modern-financial-analytics-pipeline
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

or, on Windows:

```bash
py -m pip install -r requirements.txt
```

---

### 3. Generate sample raw data

```bash
python src/generate_sample_data.py
```

or:

```bash
py src/generate_sample_data.py
```

This generates full raw datasets under:

```text
data/raw/
```

and small review samples under:

```text
data/sample/
```

---

### 4. Transform raw data

```bash
python src/transform.py
```

or:

```bash
py src/transform.py
```

This generates processed datasets under:

```text
data/processed/
```

---

### 5. Run data quality validations

```bash
python src/validate.py
```

or:

```bash
py src/validate.py
```

Validation results are printed in the terminal.

---

## Versioning Strategy

The project intentionally does not version generated raw or processed files.

Ignored folders:

```text
data/raw/
data/processed/
```
24
Reason:

These files are generate0d outputs and can be recreated by running the pipeline scripts.

```text
data/validation/
```

Reason:

Validation output files are generated artifacts and can be recreated by running `src/validate.py`.

Versioned sample files:

```text
data/sample/
```

Reason:

Small sample files are included so that reviewers can inspect the structure of the generated data directly in GitHub.

---

Ignored database outputs:

```text
data/database/
```

Reason:

The SQLite database is a generated artifact and can be recreated by running `src/load_to_sqlite.py`.

Ignored analytics outputs:

```text
data/analytics/
```

Reason:

Analytics CSV outputs are generated artifacts and can be recreated by running `src/run_sqlite_analytics.py`.

## Key Data Quality Rules

Examples of implemented validation rules:

- Customer IDs must be unique.
- Loan IDs must be unique.
- Payment IDs must be unique.
- Loan amounts must be greater than zero.
- Payment amounts cannot be negative.
- Days late cannot be negative.
- Every loan must reference a valid customer.
- Every loan must reference a valid product.
- Every loan must reference a valid branch.
- Every loan must reference a valid advisor.
- Every payment must reference a valid loan.
- Payments cannot occur before loan disbursement.
- Missed payments must have zero payment amount.
- Paid payments must have zero days late.

---

## Professional Skills Demonstrated

This project demonstrates practical skills in:

- Python-based data processing
- Data pipeline design
- SQL data quality checks
- SQL analytical queries
- Financial data modeling
- Data quality validation
- Referential integrity checks
- Business rule documentation
- Technical documentation
- Git and GitHub workflow
- Portfolio project structuring

---

## Future Improvements

Planned improvements include:

1. Add a database loading layer.
2. Load processed data into SQL Server, PostgreSQL, or Snowflake.
3. Convert transformation logic into dbt models.
4. Add dbt tests and documentation.
5. Build a Power BI dashboard.
6. Add validation reports as CSV outputs.
7. Add Airflow orchestration.
8. Add Docker for reproducible execution.
9. Add GitHub Actions for automated validation.
10. Add AI-assisted documentation or data quality summaries.

---

## Professional Purpose

This project is part of a professional transition toward modern Data Engineering, Analytics Engineering, Cloud Analytics, and Data & AI Consulting.

The objective is to demonstrate how financial data can be transformed into reliable, documented, and business-ready analytics solutions.

---

## Author

Rene Garcia-Salas  
Bilingual Data & Analytics Professional

