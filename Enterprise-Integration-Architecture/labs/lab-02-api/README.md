# Lab 2 — API-based orders

## Lab Overview

Build a synchronous order API: Client → API Gateway → Lambda → DynamoDB with validation, errors, IAM, and correlation IDs.

## Business Scenario

Harbor Retail needs `POST /orders` and `GET /orders/{id}` for mobile. Timeouts happen. Duplicate charges are unacceptable.

## Architecture

See `diagrams/02-api-integration.md`. Style: **API** (request/reply). Idempotency is mandatory.

## Learning Objectives

- Implement POST/GET with schema validation and a stable error envelope.
- Honor `Idempotency-Key`.
- Propagate `x-correlation-id`.
- Use least-privilege IAM.

## Prerequisites

Module 2. AWS CLI, Terraform ≥ 1.5, Python 3.11+. Sandbox account.

## AWS Services Used

API Gateway HTTP API, Lambda, DynamoDB, IAM, CloudWatch Logs.

## Estimated Time

2.5–3.5 hours.

## Estimated AWS Cost

**< $0.20** for a lab session if you destroy afterward. No NAT, no Transfer Family.

## Step 1 — Setup

```bash
cp terraform/labs/lab-02-api/terraform.tfvars.example terraform/labs/lab-02-api/terraform.tfvars
aws sts get-caller-identity
```

## Step 2 — Infrastructure

```bash
./scripts/lab_up.sh lab-02-api
```

## Step 3 — Application

Code lives in `lambda/lab02_orders/handler.py`. Read it before changing it.

## Step 4 — Integration

```bash
ENDPOINT=$(terraform -chdir=terraform/labs/lab-02-api output -raw api_endpoint)
KEY=$(uuidgen)
curl -sS -X POST "$ENDPOINT/orders" \
  -H "content-type: application/json" \
  -H "Idempotency-Key: $KEY" \
  -H "x-correlation-id: lab2-demo" \
  -d '{"customerId":"cust-1","amount":19.99}'
```

Retry the same key. You should see replay, not a second order.

## Step 5 — Testing

```bash
./scripts/validate_lab.py lab-02-api
```

Expect **PASS**.

## Step 6 — Failure Testing

1. POST without Idempotency-Key → 400.
2. POST amount as `"1,000"` → 422.
3. Same key, different amount → 409.
4. GET unknown id → 404 with correlation ID.

## Step 7 — Observability

In CloudWatch Logs, find `lab2-demo` in JSON. Note the field name `correlationId`.

## Step 8 — Security Review

Open the IAM policy. Confirm it cannot `DeleteTable` or access other tables. Confirm no `*` on DynamoDB actions beyond this table ARN.

## Step 9 — Architecture Questions

1. Why is this not a queue?
2. Would you put a 25 GB image in this POST? Which challenge answers that?
3. Write a four-sentence ADR fragment for idempotency keys vs client-assigned order IDs.

## Step 10 — Cleanup

```bash
./scripts/lab_down.sh lab-02-api
```
