# Project Architecture

## Project Name

Modern Financial Analytics Pipeline

## Purpose

This project demonstrates a modern data analytics workflow for a financial or microfinance business scenario.

The objective is to transform raw operational data into clean, validated, analytics-ready datasets that can support executive reporting, portfolio monitoring, data quality checks, and business decision-making.

## High-Level Workflow

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

## Architecture Layers

### 1. Sample Data Generation Layer

Script:

`src/generate_sample_data.py`

Purpose:

Generates simulated financial and microfinance datasets for customers, branches, advisors, products, loans, and payments.

This allows the project to be reproducible without relying on private or sensitive financial data.

Generated outputs:

```text
data/raw/customers.csv
data/raw/branches.csv
data/raw/advisors.csv
data/raw/products.csv
data/raw/loans.csv
data/raw/payments.csv
```

Sample files are also generated under:

`data/sample/`

These sample files are included in the repository for portfolio review.

---

### 2. Raw Data Layer

Folder:

`data/raw/`

Purpose:

Stores locally generated raw datasets.

These files represent the source operational data before transformation. They are not versioned in GitHub because they can be regenerated using the sample data generation script.

Versioning decision:

`data/raw/` is ignored through `.gitignore`.

Reason:

Raw generated data should not unnecessarily increase repository size or create version noise.

---

### 3. Processed Data Layer

Folder:

`data/processed/`

Purpose:

Stores cleaned and standardized datasets created by the transformation script.

Generated outputs:

```text
customers_processed.csv
branches_processed.csv
advisors_processed.csv
products_processed.csv
loans_processed.csv
payments_processed.csv
```

These files are also ignored by Git because they are generated outputs.

---

### 4. Python Transformation Layer

Script:

`src/transform.py`

Purpose:

Reads raw CSV files from `data/raw/`, applies standardization and cleaning rules, and writes processed CSV files into `data/processed/`.

Main responsibilities:

- Standardize column names.
- Trim text values.
- Convert date fields.
- Convert numeric fields.
- Save processed datasets.

Design rationale:

The transformation logic is separated from data generation and validation to keep the pipeline modular, reproducible, and easier to maintain.

---

### 5. Python Data Quality Validation Layer

Script:

`src/validate.py`

Purpose:

Validates processed datasets using Python-based data quality checks.

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

Design rationale:

Validation results are saved as structured output files to support auditability, review, and future integration with dashboards, orchestration tools, or automated quality monitoring.

Python validation provides a flexible programmatic layer to identify data quality issues before analytical modeling and reporting.

---

## Local Database Layer

The local database layer loads processed datasets into a SQLite database.

Script:

```text
src/load_to_sqlite.py
```

Input:

```text
data/processed/
```

Output:

```text
data/database/financial_analytics.db
```

Purpose:

This layer demonstrates how processed files can be loaded into a relational database structure for SQL-based analysis.

Design rationale:

SQLite is used as a lightweight local database option because it does not require external infrastructure. It allows the project to demonstrate a database loading layer while keeping the environment simple and reproducible.

Future versions of this layer could be migrated to SQL Server, PostgreSQL, Snowflake, or another cloud data warehouse.

---

## SQLite Analytics Output Layer

The SQLite analytics layer executes selected SQL queries against the local database and exports the results as dashboard-ready CSV files.

Script:

```text
src/run_sqlite_analytics.py
```

Input:

```text
data/database/financial_analytics.db
```

Output:

```text
data/analytics/
```

Purpose:

This layer converts relational database tables into analytics-ready outputs that can be consumed by BI tools such as Power BI.

Design rationale:

The analytics output layer separates source tables from reporting datasets. This makes the pipeline easier to maintain and prepares the project for future dashboard development.

### 6. SQL Data Quality Layer

Script:

`sql/data_quality_checks.sql`

Purpose:

Provides SQL-based validation checks that can be executed against database tables.

Validation logic:

Each SQL query is designed to return problematic records. If a query returns zero rows, the validation passes.

This layer demonstrates how data quality controls can also be implemented directly in a relational database or cloud data warehouse environment.

---

### 7. SQL Analytics Layer

Script:

`sql/analytics_queries.sql`

Purpose:

Provides analytical SQL queries for financial and microfinance reporting.

Analysis areas:

- Executive portfolio KPIs
- Loan status distribution
- Payment behavior
- Branch performance
- Advisor performance
- Product performance
- Customer segment analysis
- Monthly trends
- Recovery analysis
- Power BI-ready analytical datasets

Design rationale:

This layer translates validated data into business-oriented metrics and reporting datasets.

---

### 8. Dashboard / Reporting Layer

Folder:

`dashboards/powerbi/`

Purpose:

Reserved for future Power BI dashboard files, screenshots, and dashboard documentation.

Planned dashboard focus:

- Total loan portfolio
- Disbursed amount
- Delinquency rate
- Payment performance
- Recovery ratio
- Branch performance
- Advisor performance
- Monthly loan and payment trends

---

## Current Pipeline Status

| Layer | Status |
|---|---|
| Sample data generation | Completed |
| Raw data layer | Completed |
| Sample data for portfolio review | Completed |
| Python transformation | Completed |
| Processed data layer | Completed |
| Python validation | Completed |
| SQL data quality checks | Completed |
| SQL analytics queries | Completed |
| Power BI dashboard | Pending |
| dbt models | Future phase |
| Snowflake/cloud warehouse | Future phase |
| Airflow orchestration | Future phase |
| Docker environment | Future phase |

## Future Architecture Improvements

Planned improvements:

1. Add a database loading layer.
2. Add dbt models for staging, intermediate, and mart layers.
3. Add dbt tests and documentation.
4. Add Snowflake or another cloud warehouse.
5. Add Airflow orchestration.
6. Add Docker for reproducible local execution.
7. Add Power BI dashboard documentation.
8. Add automated data quality reporting.
9. Add CI/CD checks using GitHub Actions.

## Professional Relevance

This architecture demonstrates core skills related to:

- Data Engineering
- Analytics Engineering
- Data Quality
- Financial Analytics
- SQL-based analysis
- Python-based data processing
- Business rule validation
- Technical documentation
- Portfolio-ready project design