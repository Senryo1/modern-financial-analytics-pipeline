# Business Rules

## Project Name

Modern Financial Analytics Pipeline

## Purpose

This document describes the business and data quality rules applied in the project.

The rules are used to validate financial and microfinance datasets related to customers, loans, payments, branches, advisors, and products.

---

## Rule Categories

| Category | Purpose |
|---|---|
| Primary key rules | Ensure entity uniqueness |
| Critical field rules | Ensure mandatory fields are populated |
| Numeric rules | Ensure financial values are valid |
| Allowed value rules | Ensure categorical consistency |
| Referential integrity rules | Ensure relationships between datasets are valid |
| Business consistency rules | Ensure business logic is respected |
| Financial consistency rules | Ensure financial metrics are reasonable |

---

## 1. Primary Key Rules

### Rule 1.1: Customer ID must be unique

Each customer must have a unique `customer_id`.

Impact:

Duplicate customers can distort customer counts, segmentation, and loan relationship analysis.

Validation:

- Python: `check_duplicates(customers, ["customer_id"])`
- SQL: duplicate check grouped by `customer_id`

---

### Rule 1.2: Branch ID must be unique

Each branch must have a unique `branch_id`.

Impact:

Duplicate branches can distort regional and branch-level performance analysis.

Validation:

- Python: `check_duplicates(branches, ["branch_id"])`
- SQL: duplicate check grouped by `branch_id`

---

### Rule 1.3: Advisor ID must be unique

Each advisor must have a unique `advisor_id`.

Impact:

Duplicate advisors can distort advisor performance, accountability, and portfolio assignment.

Validation:

- Python: `check_duplicates(advisors, ["advisor_id"])`
- SQL: duplicate check grouped by `advisor_id`

---

### Rule 1.4: Product ID must be unique

Each financial product must have a unique `product_id`.

Impact:

Duplicate products can distort product-level reporting and delinquency analysis.

Validation:

- Python: `check_duplicates(products, ["product_id"])`
- SQL: duplicate check grouped by `product_id`

---

### Rule 1.5: Loan ID must be unique

Each loan must have a unique `loan_id`.

Impact:

Duplicate loans can inflate portfolio totals, disbursement metrics, and exposure calculations.

Validation:

- Python: `check_duplicates(loans, ["loan_id"])`
- SQL: duplicate check grouped by `loan_id`

---

### Rule 1.6: Payment ID must be unique

Each payment transaction must have a unique `payment_id`.

Impact:

Duplicate payments can overstate recovery, payment volume, and collection performance.

Validation:

- Python: `check_duplicates(payments, ["payment_id"])`
- SQL: duplicate check grouped by `payment_id`

---

## 2. Critical Field Rules

### Rule 2.1: Customers must have critical identification fields

Each customer record must include:

- `customer_id`
- `customer_name`
- `registration_date`
- `customer_segment`

Impact:

Missing customer information limits customer segmentation, relationship analysis, and borrower-level reporting.

---

### Rule 2.2: Branches must have critical location fields

Each branch record must include:

- `branch_id`
- `branch_name`
- `region`
- `city`

Impact:

Missing branch fields limit geographic, regional, and operational performance analysis.

---

### Rule 2.3: Advisors must have a valid branch assignment

Each advisor record must include:

- `advisor_id`
- `advisor_name`
- `branch_id`
- `hire_date`

Impact:

Missing advisor assignments break branch and advisor performance reporting.

---

### Rule 2.4: Financial products must include product metadata

Each product must include:

- `product_id`
- `product_name`
- `product_type`
- `interest_rate`

Impact:

Missing product data limits product-level portfolio analysis and financial interpretation.

---

### Rule 2.5: Loans must have all critical identifiers and financial fields

Each loan must include:

- `loan_id`
- `customer_id`
- `product_id`
- `branch_id`
- `advisor_id`
- `disbursement_date`
- `loan_amount`
- `loan_term_months`
- `loan_status`

Impact:

Missing loan fields break relationships with customers, products, branches, advisors, and financial reporting metrics.

---

### Rule 2.6: Payments must have transaction-level critical fields

Each payment must include:

- `payment_id`
- `loan_id`
- `payment_date`
- `payment_amount`
- `payment_status`
- `days_late`

Impact:

A payment without critical transaction details cannot be assigned, validated, or analyzed reliably.

---

## 3. Numeric Rules

### Rule 3.1: Loan amount must be greater than zero

A loan cannot have zero or negative original amount.

Validation:

```text
loan_amount > 0
```

Impact:

Invalid loan amounts distort portfolio totals, averages, exposure metrics, and loan-level analysis.

---

### Rule 3.2: Loan term must be greater than zero

A loan must have a positive term in months.

Validation:

```text
loan_term_months > 0
```

Impact:

Invalid loan terms affect repayment logic, maturity analysis, and portfolio duration interpretation.

---

### Rule 3.3: Interest rate cannot be negative

A financial product cannot have a negative interest rate in this simplified scenario.

Validation:

```text
interest_rate >= 0
```

Impact:

Negative interest rates would distort product and profitability assumptions.

---

### Rule 3.4: Payment amount cannot be negative

Payment amounts must be zero or positive.

Validation:

```text
payment_amount >= 0
```

Impact:

Negative payments can distort recovery, collection, and outstanding balance metrics.

---

### Rule 3.5: Days late cannot be negative

Days late must be zero or positive.

Validation:

```text
days_late >= 0
```

Impact:

Negative delay values are not logically valid for delinquency analysis.

---

## 4. Allowed Value Rules

### Rule 4.1: Gender must use allowed categories

Allowed values:

```text
F
M
```

Purpose:

Keeps demographic segmentation consistent.

---

### Rule 4.2: Customer segment must use allowed categories

Allowed values:

```text
Individual
Small Business
Microenterprise
```

Purpose:

Ensures consistent portfolio segmentation.

---

### Rule 4.3: Loan status must use allowed categories

Allowed values:

```text
Active
Closed
Delinquent
```

Purpose:

Ensures consistent loan portfolio classification.

---

### Rule 4.4: Payment status must use allowed categories

Allowed values:

```text
Paid
Late
Missed
```

Purpose:

Ensures consistent payment behavior analysis.

---

## 5. Referential Integrity Rules

### Rule 5.1: Every loan must reference a valid customer

Each `loans.customer_id` must exist in `customers.customer_id`.

Impact:

Loans without customers cannot be analyzed by borrower, customer segment, or customer-level behavior.

---

### Rule 5.2: Every loan must reference a valid product

Each `loans.product_id` must exist in `products.product_id`.

Impact:

Loans without valid product references cannot be analyzed by product type, interest rate, or product-level performance.

---

### Rule 5.3: Every loan must reference a valid branch

Each `loans.branch_id` must exist in `branches.branch_id`.

Impact:

Loans without branches cannot support branch, regional, or geographic analysis.

---

### Rule 5.4: Every loan must reference a valid advisor

Each `loans.advisor_id` must exist in `advisors.advisor_id`.

Impact:

Loans without advisors cannot support accountability, advisor performance, or portfolio ownership analysis.

---

### Rule 5.5: Every advisor must reference a valid branch

Each `advisors.branch_id` must exist in `branches.branch_id`.

Impact:

Advisors without branches cannot be included correctly in branch performance or staffing analysis.

---

### Rule 5.6: Every payment must reference a valid loan

Each `payments.loan_id` must exist in `loans.loan_id`.

Impact:

Payments without valid loan references cannot be assigned to a portfolio, customer, branch, advisor, or product.

---

## 6. Business Consistency Rules

### Rule 6.1: Payment date must not be before disbursement date

A payment cannot occur before the loan was disbursed.

Validation:

```text
payment_date >= disbursement_date
```

Impact:

Payments before disbursement indicate invalid transaction timing or source data errors.

---

### Rule 6.2: Missed payments must have zero payment amount

If `payment_status = Missed`, then `payment_amount` must be zero.

Validation:

```text
payment_status = "Missed" -> payment_amount = 0
```

Impact:

A missed payment with a positive amount creates inconsistent recovery reporting.

---

### Rule 6.3: Paid payments must have zero days late

If `payment_status = Paid`, then `days_late` must be zero.

Validation:

```text
payment_status = "Paid" -> days_late = 0
```

Impact:

A paid payment with days late greater than zero should be classified as late, not paid.

---

### Rule 6.4: Late payments must have days late greater than zero

If `payment_status = Late`, then `days_late` should be greater than zero.

Validation:

```text
payment_status = "Late" -> days_late > 0
```

Impact:

A late payment with zero delay is inconsistent with delinquency reporting.

---

### Rule 6.5: Delinquent loans should have late or missed payment behavior

If `loan_status = Delinquent`, the loan should generally have at least one late or missed payment.

Validation logic:

```text
loan_status = "Delinquent" -> at least one related payment_status in ("Late", "Missed")
```

Impact:

A delinquent loan without late or missed payment behavior may indicate inconsistent classification or incomplete payment history.

Note:

In a real institution, delinquency classification may depend on installment schedules, days past due, grace periods, restructuring, write-offs, or regulatory definitions.

---

## 7. Financial Consistency Rules

### Rule 7.1: Total paid amount should not exceed original loan amount

The total amount paid for a loan should not exceed the original loan amount in this simplified scenario.

Validation:

```text
SUM(payment_amount) <= loan_amount
```

Impact:

Overpayment can distort recovery ratios and outstanding balance estimates.

Note:

In a real financial institution, this rule would need to consider interest, fees, penalties, refinancing, write-offs, overpayment policies, and accounting treatment.

---

### Rule 7.2: Loans with no payments should be reviewed

A loan with no payments may be valid if recently disbursed, but it should be reviewed for portfolio monitoring.

Impact:

Loans with no payments may indicate new loans, missing payment data, source system delays, or collection issues.

---

### Rule 7.3: Payments with unusually high days late should be reviewed

Payments with `days_late > 120` should be flagged for review.

Validation:

```text
days_late > 120
```

Impact:

High days late values may indicate serious delinquency, data entry errors, or portfolio risk requiring review.

---

## 8. Analytical Reconciliation Rules

### Rule 8.1: Loan portfolio summaries should reconcile by status

Loan counts and loan amounts grouped by `loan_status` should reconcile with total portfolio counts and amounts.

Purpose:

Ensures that executive reporting metrics align with detailed loan-level records.

---

### Rule 8.2: Payment summaries should reconcile by status

Payment counts and payment amounts grouped by `payment_status` should reconcile with total payment records.

Purpose:

Ensures that collection and payment performance metrics align with transaction-level data.

---

### Rule 8.3: Branch portfolio summaries should reconcile with loan-level data

Loan counts and total loan amounts by branch should reconcile with the loan portfolio table.

Purpose:

Ensures branch-level reporting is consistent with loan-level source data.

---

## 9. Professional Notes

These rules are intentionally designed to demonstrate how data quality logic connects technical validation with business interpretation.

The current implementation includes both Python-based validations and SQL-based validations.

In future phases, these rules can be implemented or extended as:

- dbt tests
- SQL constraints
- Great Expectations suites
- automated validation reports
- Airflow validation tasks
- Power BI data quality indicators
- GitHub Actions validation checks
- warehouse-level monitoring rules