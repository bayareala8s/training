# Deploy & Teardown Scripts

Scripts to deploy and destroy **all course lab AWS resources** with one command.

## Quick Reference — Lab Cycle (recommended)

| Command | Purpose |
|---------|---------|
| `./scripts/lab-cycle.sh start` | **Start** — deploy stack, seed data, smoke-test |
| `./scripts/lab-cycle.sh stop --yes` | **Stop** — destroy stack + cleanup KMS/IAM/logs |
| `./scripts/lab-cycle.sh status` | **Status** — what's running, cost risk |
| `./scripts/lab-cycle.sh restart --yes` | **Restart** — fresh environment |
| `./scripts/lab-cycle.sh verify` | Health-check (stack must be running) |

```bash
# Typical workflow
./scripts/lab-cycle.sh start
source ./scripts/lab-env.sh
# ... run labs / demos (docs/LAB-DEMO-GUIDE.md) ...
./scripts/lab-cycle.sh stop --yes    # zero ongoing cost
```

## Individual Scripts

| Script | Purpose |
|--------|---------|
| `./scripts/lab-cycle.sh` | **Unified start/stop/status** (use this) |
| `./scripts/start-labs.sh` | Deploy only (called by `lab-cycle start`) |
| `./scripts/stop-labs.sh` | Terraform destroy only |
| `./scripts/cleanup-lab-extras.sh` | Remove Lab 7 KMS/IAM + leftover log groups |
| `./scripts/status-labs.sh` | Report running resources |
| `./scripts/ensure-labs-running.sh` | Deploy + smoke-test (keeps running) |
| `./scripts/verify-labs.sh` | Health-check deployed resources |
| `./scripts/lab-env.sh` | `source` to load `$BUCKET`, `$GLUE_JOB`, etc. |
| `./scripts/test-all-labs.sh` | Full E2E validation (~40 min, tears down) |

## Zero-Cost When Stopped

When you run `./scripts/lab-cycle.sh stop --yes`:

| Resource | Action |
|----------|--------|
| S3 data lake | Emptied + deleted |
| Lambda (×4) | Destroyed |
| Glue job + crawler | Destroyed |
| Step Functions | Destroyed |
| CloudWatch dashboard + alarms | Destroyed |
| SNS topics | Destroyed |
| Lab 7 IAM roles | Deleted |
| Lab 7 KMS key | Scheduled deletion (7-day AWS minimum) |
| Lambda log groups | Deleted |

**Note:** KMS keys cannot be deleted instantly in AWS — they incur ~$1/month for up to 7 days after `stop`, then $0.

## Prerequisites

1. Complete [setup/SETUP.md](../setup/SETUP.md)
2. AWS CLI configured: `aws sts get-caller-identity`
3. Terraform >= 1.5 installed
4. Python 3.10+ with `pip install -r requirements.txt`

## First-Time Setup

```bash
cd infrastructure/environments/dev
cp terraform.tfvars.example terraform.tfvars
# Edit alert_email in terraform.tfvars if using monitoring SNS
```

## Cost While Running

| Scenario | Approx. cost |
|----------|----------------|
| Stack running, schedules **off**, no manual Glue/SFN runs | ~$0.01/day (S3 storage only) |
| One Glue job run | ~$0.44 (2× G.1X × 10 min) |
| One Step Functions execution | Glue cost + pennies |
| Schedules **on** 24h | $1–5+/day |

**Always run `./scripts/lab-cycle.sh stop --yes` when finished.**

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `AccessDenied` on apply | Attach [setup/iam-policy.json](../setup/iam-policy.json) |
| S3 bucket not empty on destroy | `stop-labs.sh` empties versioned objects automatically |
| KMS key still billing after stop | AWS 7-day deletion window — check `status-labs.sh` |
| `BUCKET` empty after start | Run `lab-cycle.sh start` then `source lab-env.sh` |

## Step-by-Step Lab Demos

**[docs/LAB-DEMO-GUIDE.md](../docs/LAB-DEMO-GUIDE.md)** — all 26 labs

## CI / Quality Checks

GitHub Actions runs on push (`.github/workflows/validate.yml`):

- `terraform fmt -check` and `terraform validate`
- `pytest` for Lab 4.1 validators
- `shellcheck` on `scripts/*.sh`

Optional local pre-commit: `pip install pre-commit && pre-commit install`
