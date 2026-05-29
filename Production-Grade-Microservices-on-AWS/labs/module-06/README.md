# Lab 6 — Data Management & Consistency

**Duration:** 4 hours | **Module 6**

## Objectives

- Apply database-per-service
- Use DynamoDB for orders (AWS) while keeping SQLite locally
- Document eventual consistency strategy

## Part A — Data Ownership (45 min)

Update your decomposition doc:

- Which service owns `orders` data?
- Can product-service read order tables directly? (No — explain why)

## Part B — DynamoDB Orders (AWS) (120 min)

Terraform creates `ms-course-dev-orders` table.

Implement adapter in order-service (extension file `app/dynamodb_repo.py`):

- `put_order(order)` on create
- `get_order(order_id)` on read

Use `boto3` with IAM task role (no keys in container).

## Part C — Stock Consistency (90 min)

**Challenge:** Order service checks stock via product API but does not decrement stock.

Design one approach:

1. **Saga** — reserve → commit → compensate
2. **Eventual** — `OrderPlaced` → product service decrements stock

Write 1-page design in `docs/your-name/consistency-design.md`.

Optional: implement stock decrement on `OrderPlaced` in product-service.

## Part D — RDS Option (45 min)

Read-only: when would you choose RDS over DynamoDB for catalog?

## Verify your work

```bash
./labs/module-06/verify.sh
```

## Deliverables

- [ ] Consistency design document
- [ ] DynamoDB integration OR documented plan with timeline
- [ ] Updated ER diagram per service (not one global DB)
