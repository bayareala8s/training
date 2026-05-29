# Lab 7 — Security & Identity

**Duration:** 4 hours | **Module 7**

## Objectives

- Secure APIs with JWT
- Store secrets in AWS Secrets Manager
- Apply least-privilege IAM roles for ECS tasks

## Part A — JWT Flow (90 min)

1. Login via user-service → receive token
2. Add dependency to product-service (extension):

```python
# Protect POST /products with Bearer token
```

3. Document token lifetime and refresh strategy (design only is OK for this lab)

## Part B — Secrets Manager (90 min)

1. Create secret `ms-course/dev/jwt-secret`
2. Update ECS task definition to inject secret as env var
3. Remove hardcoded `JWT_SECRET` from task definition JSON

## Part C — IAM Task Roles (60 min)

- **Execution role:** pull from ECR, write logs
- **Task role:** `events:PutEvents`, `dynamodb:*` on orders table only

Attach task role to order-service task.

## Part D — Network Security (30 min)

Document security groups:

- ALB → ECS tasks only on app ports
- ECS → AWS APIs via NAT
- No public IPs on tasks

## Verify your work

```bash
./labs/module-07/verify.sh
```

## Deliverables

- [ ] JWT login demo recorded or scripted
- [ ] Secrets Manager in use (screenshot redacted)
- [ ] IAM policy JSON for order-service task role
- [ ] Security checklist completed (`templates/security-checklist.md`)
