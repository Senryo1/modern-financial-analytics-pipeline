/*
===============================================================================
Analytics Queries
Project: Modern Financial Analytics Pipeline

Purpose:
This script contains analytical SQL queries for financial and microfinance
portfolio reporting.

Expected tables:
- customers
- branches
- advisors
- products
- loans
- payments

Use cases:
- Executive reporting
- Portfolio monitoring
- Branch performance
- Advisor performance
- Payment behavior
- Delinquency monitoring
- Power BI semantic model preparation
===============================================================================
*/


/*
===============================================================================
1. EXECUTIVE PORTFOLIO KPIS
===============================================================================
*/


-- 1.1 Total loan portfolio
SELECT
    COUNT(*) AS total_loans,
    SUM(loan_amount) AS total_disbursed_amount,
    AVG(loan_amount) AS average_loan_amount,
    MIN(loan_amount) AS minimum_loan_amount,
    MAX(loan_amount) AS maximum_loan_amount
FROM loans;


-- 1.2 Loan portfolio by status
SELECT
    loan_status,
    COUNT(*) AS loan_count,
    SUM(loan_amount) AS total_loan_amount,
    AVG(loan_amount) AS average_loan_amount
FROM loans
GROUP BY loan_status
ORDER BY total_loan_amount DESC;


-- 1.3 Payment portfolio summary
SELECT
    COUNT(*) AS total_payments,
    SUM(payment_amount) AS total_payment_amount,
    AVG(payment_amount) AS average_payment_amount,
    AVG(days_late) AS average_days_late
FROM payments;


-- 1.4 Payment status distribution
SELECT
    payment_status,
    COUNT(*) AS payment_count,
    SUM(payment_amount) AS total_payment_amount,
    AVG(days_late) AS average_days_late
FROM payments
GROUP BY payment_status
ORDER BY payment_count DESC;


/*
===============================================================================
2. PORTFOLIO PERFORMANCE BY BRANCH
===============================================================================
*/


-- 2.1 Loan portfolio by branch
SELECT
    b.branch_id,
    b.branch_name,
    b.region,
    b.city,
    COUNT(l.loan_id) AS loan_count,
    SUM(l.loan_amount) AS total_loan_amount,
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


-- 2.2 Delinquent portfolio by branch
SELECT
    b.branch_id,
    b.branch_name,
    b.region,
    COUNT(l.loan_id) AS total_loans,
    SUM(
        CASE
            WHEN l.loan_status = 'Delinquent' THEN 1
            ELSE 0
        END
    ) AS delinquent_loans,
    SUM(
        CASE
            WHEN l.loan_status = 'Delinquent' THEN l.loan_amount
            ELSE 0
        END
    ) AS delinquent_amount,
    CAST(
        SUM(
            CASE
                WHEN l.loan_status = 'Delinquent' THEN 1
                ELSE 0
            END
        ) AS FLOAT
    ) / NULLIF(COUNT(l.loan_id), 0) AS delinquency_rate
FROM branches b
LEFT JOIN loans l
    ON b.branch_id = l.branch_id
GROUP BY
    b.branch_id,
    b.branch_name,
    b.region
ORDER BY delinquency_rate DESC;


/*
===============================================================================
3. ADVISOR PERFORMANCE
===============================================================================
*/


-- 3.1 Loan portfolio by advisor
SELECT
    a.advisor_id,
    a.advisor_name,
    b.branch_name,
    COUNT(l.loan_id) AS loan_count,
    SUM(l.loan_amount) AS total_loan_amount,
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


-- 3.2 Advisor delinquency performance
SELECT
    a.advisor_id,
    a.advisor_name,
    b.branch_name,
    COUNT(l.loan_id) AS total_loans,
    SUM(
        CASE
            WHEN l.loan_status = 'Delinquent' THEN 1
            ELSE 0
        END
    ) AS delinquent_loans,
    CAST(
        SUM(
            CASE
                WHEN l.loan_status = 'Delinquent' THEN 1
                ELSE 0
            END
        ) AS FLOAT
    ) / NULLIF(COUNT(l.loan_id), 0) AS delinquency_rate,
    SUM(
        CASE
            WHEN l.loan_status = 'Delinquent' THEN l.loan_amount
            ELSE 0
        END
    ) AS delinquent_amount
FROM advisors a
LEFT JOIN branches b
    ON a.branch_id = b.branch_id
LEFT JOIN loans l
    ON a.advisor_id = l.advisor_id
GROUP BY
    a.advisor_id,
    a.advisor_name,
    b.branch_name
ORDER BY delinquency_rate DESC;


/*
===============================================================================
4. PRODUCT PERFORMANCE
===============================================================================
*/


-- 4.1 Loan portfolio by product
SELECT
    p.product_id,
    p.product_name,
    p.product_type,
    p.interest_rate,
    COUNT(l.loan_id) AS loan_count,
    SUM(l.loan_amount) AS total_loan_amount,
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


-- 4.2 Delinquency by product
SELECT
    p.product_id,
    p.product_name,
    COUNT(l.loan_id) AS total_loans,
    SUM(
        CASE
            WHEN l.loan_status = 'Delinquent' THEN 1
            ELSE 0
        END
    ) AS delinquent_loans,
    CAST(
        SUM(
            CASE
                WHEN l.loan_status = 'Delinquent' THEN 1
                ELSE 0
            END
        ) AS FLOAT
    ) / NULLIF(COUNT(l.loan_id), 0) AS delinquency_rate,
    SUM(
        CASE
            WHEN l.loan_status = 'Delinquent' THEN l.loan_amount
            ELSE 0
        END
    ) AS delinquent_amount
FROM products p
LEFT JOIN loans l
    ON p.product_id = l.product_id
GROUP BY
    p.product_id,
    p.product_name
ORDER BY delinquency_rate DESC;


/*
===============================================================================
5. CUSTOMER SEGMENT ANALYSIS
===============================================================================
*/


-- 5.1 Loan portfolio by customer segment
SELECT
    c.customer_segment,
    COUNT(DISTINCT c.customer_id) AS customer_count,
    COUNT(l.loan_id) AS loan_count,
    SUM(l.loan_amount) AS total_loan_amount,
    AVG(l.loan_amount) AS average_loan_amount
FROM customers c
LEFT JOIN loans l
    ON c.customer_id = l.customer_id
GROUP BY c.customer_segment
ORDER BY total_loan_amount DESC;


-- 5.2 Payment behavior by customer segment
SELECT
    c.customer_segment,
    COUNT(p.payment_id) AS payment_count,
    SUM(p.payment_amount) AS total_payment_amount,
    AVG(p.payment_amount) AS average_payment_amount,
    AVG(p.days_late) AS average_days_late,
    SUM(
        CASE
            WHEN p.payment_status = 'Late' THEN 1
            ELSE 0
        END
    ) AS late_payments,
    SUM(
        CASE
            WHEN p.payment_status = 'Missed' THEN 1
            ELSE 0
        END
    ) AS missed_payments
FROM customers c
INNER JOIN loans l
    ON c.customer_id = l.customer_id
INNER JOIN payments p
    ON l.loan_id = p.loan_id
GROUP BY c.customer_segment
ORDER BY average_days_late DESC;


/*
===============================================================================
6. MONTHLY TREND ANALYSIS
===============================================================================
*/


-- 6.1 Monthly loan disbursement trend
SELECT
    DATEFROMPARTS(
        YEAR(disbursement_date),
        MONTH(disbursement_date),
        1
    ) AS disbursement_month,
    COUNT(loan_id) AS loan_count,
    SUM(loan_amount) AS total_disbursed_amount,
    AVG(loan_amount) AS average_loan_amount
FROM loans
GROUP BY
    YEAR(disbursement_date),
    MONTH(disbursement_date)
ORDER BY disbursement_month;


-- 6.2 Monthly payment trend
SELECT
    DATEFROMPARTS(
        YEAR(payment_date),
        MONTH(payment_date),
        1
    ) AS payment_month,
    COUNT(payment_id) AS payment_count,
    SUM(payment_amount) AS total_payment_amount,
    AVG(payment_amount) AS average_payment_amount,
    AVG(days_late) AS average_days_late
FROM payments
GROUP BY
    YEAR(payment_date),
    MONTH(payment_date)
ORDER BY payment_month;


-- 6.3 Monthly late and missed payment trend
SELECT
    DATEFROMPARTS(
        YEAR(payment_date),
        MONTH(payment_date),
        1
    ) AS payment_month,
    COUNT(payment_id) AS total_payments,
    SUM(
        CASE
            WHEN payment_status = 'Late' THEN 1
            ELSE 0
        END
    ) AS late_payments,
    SUM(
        CASE
            WHEN payment_status = 'Missed' THEN 1
            ELSE 0
        END
    ) AS missed_payments,
    CAST(
        SUM(
            CASE
                WHEN payment_status IN ('Late', 'Missed') THEN 1
                ELSE 0
            END
        ) AS FLOAT
    ) / NULLIF(COUNT(payment_id), 0) AS problematic_payment_rate
FROM payments
GROUP BY
    YEAR(payment_date),
    MONTH(payment_date)
ORDER BY payment_month;


/*
===============================================================================
7. COLLECTION AND RECOVERY ANALYSIS
===============================================================================
*/


-- 7.1 Total paid amount by loan
SELECT
    l.loan_id,
    l.customer_id,
    l.loan_amount,
    l.loan_status,
    COUNT(p.payment_id) AS payment_count,
    SUM(p.payment_amount) AS total_paid_amount,
    l.loan_amount - SUM(p.payment_amount) AS estimated_outstanding_amount,
    CAST(SUM(p.payment_amount) AS FLOAT) / NULLIF(l.loan_amount, 0) AS payment_to_loan_ratio
FROM loans l
LEFT JOIN payments p
    ON l.loan_id = p.loan_id
GROUP BY
    l.loan_id,
    l.customer_id,
    l.loan_amount,
    l.loan_status
ORDER BY payment_to_loan_ratio DESC;


-- 7.2 Recovery performance by branch
SELECT
    b.branch_id,
    b.branch_name,
    COUNT(DISTINCT l.loan_id) AS loan_count,
    SUM(l.loan_amount) AS total_loan_amount,
    SUM(p.payment_amount) AS total_paid_amount,
    CAST(SUM(p.payment_amount) AS FLOAT) / NULLIF(SUM(l.loan_amount), 0) AS recovery_ratio
FROM branches b
LEFT JOIN loans l
    ON b.branch_id = l.branch_id
LEFT JOIN payments p
    ON l.loan_id = p.loan_id
GROUP BY
    b.branch_id,
    b.branch_name
ORDER BY recovery_ratio DESC;


-- 7.3 Recovery performance by advisor
SELECT
    a.advisor_id,
    a.advisor_name,
    COUNT(DISTINCT l.loan_id) AS loan_count,
    SUM(l.loan_amount) AS total_loan_amount,
    SUM(p.payment_amount) AS total_paid_amount,
    CAST(SUM(p.payment_amount) AS FLOAT) / NULLIF(SUM(l.loan_amount), 0) AS recovery_ratio
FROM advisors a
LEFT JOIN loans l
    ON a.advisor_id = l.advisor_id
LEFT JOIN payments p
    ON l.loan_id = p.loan_id
GROUP BY
    a.advisor_id,
    a.advisor_name
ORDER BY recovery_ratio DESC;


/*
===============================================================================
8. POWER BI READY DATASETS
===============================================================================
*/


-- 8.1 Loan-level analytical dataset
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
    SUM(pay.payment_amount) AS total_paid_amount,
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


-- 8.2 Payment-level analytical dataset
SELECT
    pay.payment_id,
    pay.loan_id,
    l.customer_id,
    c.customer_name,
    c.customer_segment,
    l.branch_id,
    b.branch_name,
    b.region,
    l.advisor_id,
    a.advisor_name,
    pay.payment_date,
    pay.payment_amount,
    pay.payment_status,
    pay.days_late,
    l.loan_amount,
    l.loan_status
FROM payments pay
LEFT JOIN loans l
    ON pay.loan_id = l.loan_id
LEFT JOIN customers c
    ON l.customer_id = c.customer_id
LEFT JOIN branches b
    ON l.branch_id = b.branch_id
LEFT JOIN advisors a
    ON l.advisor_id = a.advisor_id;


/*
===============================================================================
End of Analytics Queries
===============================================================================
*/