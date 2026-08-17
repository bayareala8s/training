# Lab 3 — S3 event processor (Lambda)

**Week 3 · Estimated time: 4 hours**

> **Terraform:** Lambda `baylearn-mft-lab-s3-processor`, DynamoDB idempotency table, S3 notification — deployed by lab stack. Source: `app/lambdas/s3_processor/`.

## Objectives

On `ObjectCreated` under `partners/demo/inbound/`, run Lambda to validate and move files to `processing/` or `quarantine/`.

## Steps

### 1. Confirm resources

```bash
aws lambda get-function --function-name baylearn-mft-lab-s3-processor --query Configuration.FunctionName
terraform -chdir=infra/environments/lab output -raw idempotency_table
```

### 2. Test valid file

```bash
BUCKET=$(terraform -chdir=infra/environments/lab output -raw landing_bucket)
echo '{"ok":true}' > /tmp/test.json
aws s3 cp /tmp/test.json s3://${BUCKET}/partners/demo/inbound/lab03-valid.json
sleep 5
aws s3 ls s3://${BUCKET}/partners/demo/processing/
```

### 3. Test invalid file

```bash
echo bad > /tmp/test.exe
aws s3 cp /tmp/test.exe s3://${BUCKET}/partners/demo/inbound/lab03-bad.exe
sleep 5
aws s3 ls s3://${BUCKET}/partners/demo/quarantine/
```

### 4. CloudWatch Logs

```bash
aws logs tail /aws/lambda/baylearn-mft-lab-s3-processor --since 10m
```

### 5. Extension exercise

Modify `app/lambdas/s3_processor/handler.py`, then `terraform -chdir=infra/environments/lab apply` (Lambda zip hash changes).

## Deliverables

- Lambda code in `submissions/week-03/lambda/`  
- Log excerpts showing both paths  
- README: idempotency and failure behavior  

## Rubric (10 pts)

| Criterion | Points |
|-----------|--------|
| Valid file routed to processing | 3 |
| Invalid file quarantined | 3 |
| Idempotency demonstrated | 2 |
| Documentation | 2 |
