# Deploy & Teardown Scripts

Scripts to deploy and destroy **all course lab AWS resources** with one command.

## Quick Reference

| Script | Purpose |
|--------|---------|
| `./scripts/start-labs.sh` | Deploy all lab infrastructure + seed sample data |
| `./scripts/stop-labs.sh` | Tear down all resources (empty S3, terraform destroy) |
| `./scripts/verify-labs.sh` | Health-check deployed resources |
| `./scripts/deploy-verify-destroy.sh` | Deploy → verify → destroy (zero ongoing cost) |

## Prerequisites

1. Complete [setup/SETUP.md](../setup/SETUP.md)
2. AWS CLI configured: `aws sts get-caller-identity`
3. Terraform >= 1.5 installed
4. Python 3.10+ with `boto3`: `pip install -r requirements.txt`

## First-Time Setup

```bash
cd infrastructure/environments/dev
cp terraform.tfvars.example terraform.tfvars
# Edit alert_email in terraform.tfvars if using monitoring SNS
```

## Deploy All Labs

```bash
./scripts/start-labs.sh
```

This will:

1. Run preflight checks (AWS credentials, tools)
2. `terraform init && apply` — deploys:
   - S3 data lake (Week 1)
   - 3 Lambda functions + S3 notifications (Week 2)
   - Glue job, crawler, catalog (Week 3)
   - Quality validation Lambda (Week 4)
   - Step Functions state machine (Week 6)
   - CloudWatch dashboard + SNS alarms (Week 8)
3. Seed sample retail orders data (Module 1)
4. Smoke-test Lambda ingestion

**Cost note:** EventBridge schedules are **disabled by default** (`enable_schedules = false` in `terraform.tfvars`). Glue jobs only run when you start them manually.

## Verify Deployment

```bash
./scripts/verify-labs.sh
```

## Tear Down (Stop All Charges)

```bash
./scripts/stop-labs.sh
```

Or skip confirmation:

```bash
./scripts/stop-labs.sh --yes
```

## One-Shot: Deploy, Verify, Destroy

For a cost-free validation run:

```bash
./scripts/deploy-verify-destroy.sh
```

## Enable Schedules (Optional)

Edit `infrastructure/environments/dev/terraform.tfvars`:

```hcl
enable_schedules = true
```

Then re-apply. **Remember to run `stop-labs.sh` when done** — scheduled Lambdas and Step Functions will incur charges.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `AccessDenied` on apply | Attach [setup/iam-policy.json](../setup/iam-policy.json) to your IAM user |
| S3 bucket not empty on destroy | `stop-labs.sh` empties versioned objects automatically |
| Terraform state locked | Remove stale lock from S3 backend if using remote state |
| Lambda smoke test fails | Check CloudWatch Logs: `/aws/lambda/cnde-dev-file-ingest` |

## Estimated Cost

| Scenario | Cost |
|----------|------|
| Deploy + verify + destroy (same session) | ~$0.01–0.05 |
| Leave running 24h (schedules off) | ~$0 (S3 pennies only) |
| Leave running 24h (schedules on) | $1–5+ (Lambda + Glue runs) |
| Run Glue job once manually | ~$0.44 (2× G.1X DPU × 10 min) |

**Always run `./scripts/stop-labs.sh` when finished with labs.**
