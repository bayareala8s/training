# Reference — FinOps Policy Snippet (NorthStar fictional)

## Required tags

`Project`, `Course` (lab), `Module`, `Environment`, `Owner`, `CostCenter`, `ExpirationDate` (nonprod/sandbox).

## Budgets

- Sandbox: hard alert at $50/month (enterprise); lab uses $5 for teaching
- Product prod: 80% actual + 100% forecast alerts to product owner + platform

## Lifecycle

- Lab/sandbox resources destroyed within 24 hours of exercise end unless exception ticket
- S3 lab buckets lifecycle expire ≤7 days

## Enforcement

Missing tags fail CI for platform pipelines; monthly showback to BU presidents.
