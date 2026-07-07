# Data Dictionary

## Project Name

Modern Financial Analytics Pipeline

## Purpose

This document describes the datasets, fields, definitions, and business meaning used in the project.

The data model simulates a financial or microfinance portfolio with customers, loans, payments, branches, advisors, and financial products.

---

# Dataset Overview

| Dataset | Description |
|---|---|
| customers | Customer master data |
| branches | Branch or agency information |
| advisors | Credit advisor information |
| products | Financial product catalog |
| loans | Loan portfolio data |
| payments | Loan payment transaction data |

---

# 1. customers

## Description

Contains customer master data used to identify borrowers and analyze the loan portfolio by customer segment and geography.

## Fields

| Field | Type | Description | Example |
|---|---|---|---|
| customer_id | string | Unique customer identifier | C001 |
| customer_name | string | Customer full name | Ana Lopez |
| gender | string | Customer gender category | F |
| birth_date | date | Customer date of birth | 1989-04-12 |
| registration_date | date | Date when the customer was registered | 2021-01-15 |
| city | string | Customer city | Guatemala City |
| customer_segment | string | Customer business segment | Individual |

## Business Use

Used for:

- Customer segmentation
- Portfolio analysis by customer type
- Payment behavior analysis
- Relationship with loans

---

# 2. branches

## Description

Contains information about branches or agencies where loans are originated or managed.

## Fields

| Field | Type | Description | Example |
|---|---|---|---|
| branch_id | string | Unique branch identifier | B001 |
| branch_name | string | Branch name | Central Branch |
| region | string | Geographic or business region | Metropolitan |
| city | string | Branch city | Guatemala City |

## Business Use

Used for:

- Branch performance analysis
- Regional portfolio monitoring
- Delinquency analysis by branch
- Recovery performance by branch

---

# 3. advisors

## Description

Contains information about credit advisors responsible for managing customers and loans.

## Fields

| Field | Type | Description | Example |
|---|---|---|---|
| advisor_id | string | Unique advisor identifier | A001 |
| advisor_name | string | Advisor full name | Laura Ramirez |
| branch_id | string | Branch assigned to the advisor | B001 |
| hire_date | date | Advisor hire date | 2019-05-10 |

## Business Use

Used for:

- Advisor performance monitoring
- Loan origination analysis
- Delinquency by advisor
- Recovery performance by advisor

---

# 4. products

## Description

Contains the financial products offered by the institution.

## Fields

| Field | Type | Description | Example |
|---|---|---|---|
| product_id | string | Unique product identifier | P001 |
| product_name | string | Product name | Microloan Working Capital |
| product_type | string | Type of financial product | Loan |
| interest_rate | decimal | Product interest rate | 0.18 |

## Business Use

Used for:

- Product performance analysis
- Loan portfolio by product
- Delinquency by product
- Product-level profitability assumptions

---

# 5. loans

## Description

Contains loan portfolio data. Each record represents a loan granted to a customer.

## Fields

| Field | Type | Description | Example |
|---|---|---|---|
| loan_id | string | Unique loan identifier | L001 |
| customer_id | string | Customer associated with the loan | C001 |
| product_id | string | Financial product associated with the loan | P001 |
| branch_id | string | Branch where the loan is managed | B001 |
| advisor_id | string | Advisor responsible for the loan | A001 |
| disbursement_date | date | Loan disbursement date | 2023-01-15 |
| loan_amount | numeric | Original loan amount | 15000 |
| loan_term_months | integer | Loan term in months | 12 |
| loan_status | string | Current loan status | Active |

## Business Use

Used for:

- Loan portfolio analysis
- Disbursement trend analysis
- Delinquency monitoring
- Advisor and branch performance
- Product performance
- Power BI reporting layer

---

# 6. payments

## Description

Contains payment transaction data related to loans.

Each record represents a payment event associated with a loan.

## Fields

| Field | Type | Description | Example |
|---|---|---|---|
| payment_id | string | Unique payment identifier | PMT0001 |
| loan_id | string | Loan associated with the payment | L001 |
| payment_date | date | Date when the payment occurred | 2023-02-15 |
| payment_amount | numeric | Payment amount received | 1250.00 |
| payment_status | string | Payment status category | Paid |
| days_late | integer | Number of days late | 0 |

## Business Use

Used for:

- Payment behavior analysis
- Recovery analysis
- Late payment monitoring
- Missed payment monitoring
- Customer segment payment analysis
- Monthly payment trends

---

# Relationship Overview

## Main Relationships

| Child Dataset | Child Field | Parent Dataset | Parent Field | Relationship |
|---|---|---|---|---|
| loans | customer_id | customers | customer_id | Many loans can belong to one customer |
| loans | product_id | products | product_id | Many loans can belong to one product |
| loans | branch_id | branches | branch_id | Many loans can belong to one branch |
| loans | advisor_id | advisors | advisor_id | Many loans can belong to one advisor |
| advisors | branch_id | branches | branch_id | Many advisors can belong to one branch |
| payments | loan_id | loans | loan_id | Many payments can belong to one loan |

---

# Analytical Grain

## customers

One row per customer.

## branches

One row per branch.

## advisors

One row per advisor.

## products

One row per financial product.

## loans

One row per loan.

## payments

One row per payment transaction.

---

# Notes

This data dictionary is based on simulated data generated for portfolio and demonstration purposes.

The structure is designed to resemble a simplified financial analytics environment and can be extended into a dimensional model using fact and dimension tables in future phases.