/*
===============================================================================
Data Quality Checks
Project: Modern Financial Analytics Pipeline

Purpose:
This script contains SQL-based data quality checks for the processed financial
datasets used in the analytics pipeline.

Expected tables:
- customers
- branches
- advisors
- products
- loans
- payments

Validation logic:
Each query is designed to return problematic records.
If a query returns zero rows, the validation passes.
===============================================================================
*/


/*
===============================================================================
1. PRIMARY KEY DUPLICATE CHECKS
===============================================================================
*/


-- 1.1 Check duplicated customer IDs
SELECT
    customer_id,
    COUNT(*) AS record_count
FROM customers
GROUP BY customer_id
HAVING COUNT(*) > 1;


-- 1.2 Check duplicated branch IDs
SELECT
    branch_id,
    COUNT(*) AS record_count
FROM branches
GROUP BY branch_id
HAVING COUNT(*) > 1;


-- 1.3 Check duplicated advisor IDs
SELECT
    advisor_id,
    COUNT(*) AS record_count
FROM advisors
GROUP BY advisor_id
HAVING COUNT(*) > 1;


-- 1.4 Check duplicated product IDs
SELECT
    product_id,
    COUNT(*) AS record_count
FROM products
GROUP BY product_id
HAVING COUNT(*) > 1;


-- 1.5 Check duplicated loan IDs
SELECT
    loan_id,
    COUNT(*) AS record_count
FROM loans
GROUP BY loan_id
HAVING COUNT(*) > 1;


-- 1.6 Check duplicated payment IDs
SELECT
    payment_id,
    COUNT(*) AS record_count
FROM payments
GROUP BY payment_id
HAVING COUNT(*) > 1;


/*
===============================================================================
2. CRITICAL NULL VALUE CHECKS
===============================================================================
*/


-- 2.1 Customers with missing critical fields
SELECT *
FROM customers
WHERE customer_id IS NULL
   OR customer_name IS NULL
   OR registration_date IS NULL
   OR customer_segment IS NULL;


-- 2.2 Branches with missing critical fields
SELECT *
FROM branches
WHERE branch_id IS NULL
   OR branch_name IS NULL
   OR region IS NULL
   OR city IS NULL;


-- 2.3 Advisors with missing critical fields
SELECT *
FROM advisors
WHERE advisor_id IS NULL
   OR advisor_name IS NULL
   OR branch_id IS NULL
   OR hire_date IS NULL;


-- 2.4 Products with missing critical fields
SELECT *
FROM products
WHERE product_id IS NULL
   OR product_name IS NULL
   OR product_type IS NULL
   OR interest_rate IS NULL;


-- 2.5 Loans with missing critical fields
SELECT *
FROM loans
WHERE loan_id IS NULL
   OR customer_id IS NULL
   OR product_id IS NULL
   OR branch_id IS NULL
   OR advisor_id IS NULL
   OR disbursement_date IS NULL
   OR loan_amount IS NULL
   OR loan_term_months IS NULL
   OR loan_status IS NULL;


-- 2.6 Payments with missing critical fields
SELECT *
FROM payments
WHERE payment_id IS NULL
   OR loan_id IS NULL
   OR payment_date IS NULL
   OR payment_amount IS NULL
   OR payment_status IS NULL
   OR days_late IS NULL;


/*
===============================================================================
3. NUMERIC VALIDATION CHECKS
===============================================================================
*/


-- 3.1 Loans with invalid loan amount
SELECT *
FROM loans
WHERE loan_amount <= 0;


-- 3.2 Loans with invalid term
SELECT *
FROM loans
WHERE loan_term_months <= 0;


-- 3.3 Products with invalid interest rate
SELECT *
FROM products
WHERE interest_rate < 0;


-- 3.4 Payments with negative payment amount
SELECT *
FROM payments
WHERE payment_amount < 0;


-- 3.5 Payments with negative days late
SELECT *
FROM payments
WHERE days_late < 0;


/*
===============================================================================
4. ALLOWED VALUE CHECKS
===============================================================================
*/


-- 4.1 Customers with invalid gender values
SELECT *
FROM customers
WHERE gender NOT IN ('F', 'M');


-- 4.2 Customers with invalid segment values
SELECT *
FROM customers
WHERE customer_segment NOT IN (
    'Individual',
    'Small Business',
    'Microenterprise'
);


-- 4.3 Loans with invalid loan status values
SELECT *
FROM loans
WHERE loan_status NOT IN (
    'Active',
    'Closed',
    'Delinquent'
);


-- 4.4 Payments with invalid payment status values
SELECT *
FROM payments
WHERE payment_status NOT IN (
    'Paid',
    'Late',
    'Missed'
);


/*
===============================================================================
5. REFERENTIAL INTEGRITY CHECKS
===============================================================================
*/


-- 5.1 Loans without valid customer
SELECT
    l.*
FROM loans l
LEFT JOIN customers c
    ON l.customer_id = c.customer_id
WHERE c.customer_id IS NULL;


-- 5.2 Loans without valid product
SELECT
    l.*
FROM loans l
LEFT JOIN products p
    ON l.product_id = p.product_id
WHERE p.product_id IS NULL;


-- 5.3 Loans without valid branch
SELECT
    l.*
FROM loans l
LEFT JOIN branches b
    ON l.branch_id = b.branch_id
WHERE b.branch_id IS NULL;


-- 5.4 Loans without valid advisor
SELECT
    l.*
FROM loans l
LEFT JOIN advisors a
    ON l.advisor_id = a.advisor_id
WHERE a.advisor_id IS NULL;


-- 5.5 Advisors without valid branch
SELECT
    a.*
FROM advisors a
LEFT JOIN branches b
    ON a.branch_id = b.branch_id
WHERE b.branch_id IS NULL;


-- 5.6 Payments without valid loan
SELECT
    p.*
FROM payments p
LEFT JOIN loans l
    ON p.loan_id = l.loan_id
WHERE l.loan_id IS NULL;


/*
===============================================================================
6. BUSINESS RULE CHECKS
===============================================================================
*/


-- 6.1 Payments before loan disbursement date
SELECT
    p.payment_id,
    p.loan_id,
    l.disbursement_date,
    p.payment_date,
    p.payment_amount,
    p.payment_status,
    p.days_late
FROM payments p
INNER JOIN loans l
    ON p.loan_id = l.loan_id
WHERE p.payment_date < l.disbursement_date;


-- 6.2 Missed payments with payment amount different from zero
SELECT *
FROM payments
WHERE payment_status = 'Missed'
  AND payment_amount <> 0;


-- 6.3 Paid payments with days late different from zero
SELECT *
FROM payments
WHERE payment_status = 'Paid'
  AND days_late <> 0;


-- 6.4 Late payments with zero days late
SELECT *
FROM payments
WHERE payment_status = 'Late'
  AND days_late = 0;


-- 6.5 Loans marked as delinquent but without late or missed payments
SELECT
    l.loan_id,
    l.customer_id,
    l.loan_status
FROM loans l
LEFT JOIN payments p
    ON l.loan_id = p.loan_id
GROUP BY
    l.loan_id,
    l.customer_id,
    l.loan_status
HAVING l.loan_status = 'Delinquent'
   AND SUM(
        CASE
            WHEN p.payment_status IN ('Late', 'Missed') THEN 1
            ELSE 0
        END
   ) = 0;


/*
===============================================================================
7. FINANCIAL CONSISTENCY CHECKS
===============================================================================
*/


-- 7.1 Total paid amount greater than original loan amount
SELECT
    l.loan_id,
    l.loan_amount,
    SUM(p.payment_amount) AS total_paid_amount
FROM loans l
INNER JOIN payments p
    ON l.loan_id = p.loan_id
GROUP BY
    l.loan_id,
    l.loan_amount
HAVING SUM(p.payment_amount) > l.loan_amount;


-- 7.2 Loans with no payments
SELECT
    l.*
FROM loans l
LEFT JOIN payments p
    ON l.loan_id = p.loan_id
WHERE p.payment_id IS NULL;


-- 7.3 Payments with unusually high days late
SELECT *
FROM payments
WHERE days_late > 120;


/*
===============================================================================
8. ANALYTICAL RECONCILIATION CHECKS
===============================================================================
*/


-- 8.1 Loan portfolio summary by status
SELECT
    loan_status,
    COUNT(*) AS loan_count,
    SUM(loan_amount) AS total_loan_amount,
    AVG(loan_amount) AS average_loan_amount
FROM loans
GROUP BY loan_status
ORDER BY loan_status;


-- 8.2 Payment summary by status
SELECT
    payment_status,
    COUNT(*) AS payment_count,
    SUM(payment_amount) AS total_payment_amount,
    AVG(days_late) AS average_days_late
FROM payments
GROUP BY payment_status
ORDER BY payment_status;


-- 8.3 Portfolio by branch
SELECT
    b.branch_id,
    b.branch_name,
    b.region,
    COUNT(l.loan_id) AS loan_count,
    SUM(l.loan_amount) AS total_loan_amount
FROM branches b
LEFT JOIN loans l
    ON b.branch_id = l.branch_id
GROUP BY
    b.branch_id,
    b.branch_name,
    b.region
ORDER BY total_loan_amount DESC;


/*
===============================================================================
End of Data Quality Checks
===============================================================================
*/