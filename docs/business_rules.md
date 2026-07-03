
# Business Rules

This document will describe the business and data quality rules applied in the project.

## Initial Planned Rules

| Rule | Description | Impact |
|---|---|---|
| Customer ID must not be null | Every loan and payment must be linked to a customer | Referential integrity |
| Loan amount must be greater than zero | Loans cannot have negative or zero original amounts | Financial accuracy |
| Payment date must not be before loan disbursement date | Payments should occur after loan origination | Business consistency |
| Branch ID must exist in branch catalog | Each loan must be associated with a valid branch | Reporting accuracy |
| Advisor ID must exist in advisor catalog | Each loan should be linked to a valid advisor | Portfolio accountability |
