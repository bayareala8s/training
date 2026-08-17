# Lab 5 — SFTP connector flows

**Week 5 · Estimated time: 4 hours**

> **Terraform:** Self-demo connector to the same Transfer server (`enable_connector=true`). Output: `transfer_connector_id`.

## Objectives

Configure a Transfer Family **connector** and run at least one **S3 → remote SFTP** or **remote SFTP → S3** transfer.

## Steps (self-demo connector)

### 1. Get connector ID

```bash
CONNECTOR=$(terraform -chdir=infra/environments/lab output -raw transfer_connector_id)
BUCKET=$(terraform -chdir=infra/environments/lab output -raw landing_bucket)
echo "$CONNECTOR"
```

### 2. Stage outbound file

```bash
echo "payroll,data" > /tmp/outbound.csv
aws s3 cp /tmp/outbound.csv s3://${BUCKET}/partners/demo/outbound/payroll.csv
```

### 3. Start S3 → SFTP transfer (console or CLI)

Use **Transfer Family → Connectors → Start transfer**, or AWS CLI per current [StartFileTransfer](https://docs.aws.amazon.com/cli/latest/reference/transfer/start-file-transfer.html) syntax for your region.

### 4. Partner matrix deliverable

Copy [`templates/partner-matrix.csv`](../../templates/partner-matrix.csv) to `submissions/week-05/partner-matrix.csv` and add 3 partners.

## Other setup options

- **Second AWS account** as remote partner  
- **Docker OpenSSH** for local remote host  

## Deliverables

- `submissions/week-05/partner-matrix.csv`  
- Transfer log / screenshot of completed job  

## Rubric (10 pts)

| Criterion | Points |
|-----------|--------|
| Connector transfer succeeds | 5 |
| Secrets Manager used | 2 |
| Partner matrix | 3 |

## Notes

Connector egress IP and VPC alignment matter for real partners — document your setup in README.
