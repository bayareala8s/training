# BayLearn MFT — Terraform lab infrastructure

Single environment **`infra/environments/lab`** provisions **all weekly labs** (weeks 1–7) in one stack.

## What gets created

| Week | Resources |
|------|-----------|
| 1–2 | S3 landing + logs, KMS, Transfer Family SFTP, IAM |
| 3 | S3 event → Lambda processor, DynamoDB idempotency |
| 4 | Step Functions workflow, SNS topics |
| 5 | Transfer connector (self-demo to same server) |
| 6 | Cognito, HTTP API, connections/jobs DynamoDB, API Lambda |
| 7 | CloudWatch dashboard + alarms |
| **9** | VPC, ECR, ECS Fargate worker, S3→Lambda→RunTask for `large/inbound/` |

## Lab 9 — ECS Fargate

- **Worker image:** `app/workers/fargate/` → ECR via `./scripts/build_ecs_worker.sh`
- **Trigger:** S3 upload to `partners/demo/large/inbound/` (not the Lab 3 Lambda prefix)
- **Output:** `partners/demo/large/processed/` + SHA-256 manifest
- **No always-on ECS service** — cost is per task run only

## Cost control (important)

| Resource | Cost note |
|----------|-----------|
| **Transfer Family server** | ~$0.30/hour while **ONLINE** — largest lab cost |
| S3, Lambda, DynamoDB, API GW | Pay per use; low for short labs |
| **ECS Fargate (Lab 9)** | Per task minute only — no service idle cost |
| **NAT gateway** | Not used (public subnet + S3 VPC endpoint) |
| KMS | Key + API calls |

**Always destroy when done:**

```bash
./scripts/stop_stack.sh --yes
```

**Full cycle (provision → test → destroy):**

```bash
./scripts/lab_cycle.sh --yes --destroy
```

## Quick start

```bash
cp infra/environments/lab/terraform.tfvars.example infra/environments/lab/terraform.tfvars
# Edit admin_email / admin_password

./scripts/start_stack.sh --yes
./scripts/verify_labs.sh
./scripts/get_sftp_private_key.sh
./scripts/cognito_login.sh
```

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `force_destroy` | `true` | Empty buckets on destroy |
| `enable_transfer_family` | `true` | SFTP server (main cost) |
| `enable_connector` | `true` | Lab 5 connector |
| `aws_region` | `us-west-2` | Region |

Set `enable_transfer_family = false` to practice weeks 3–6 without SFTP hourly cost (weeks 1, 2, 5 SFTP labs skipped).

## Outputs

```bash
terraform -chdir=infra/environments/lab output
```

## Prerequisites

- Terraform >= 1.5
- AWS CLI v2 with credentials (`aws sts get-caller-identity`)
- `jq`, `bash`
- Outbound **ssh-keyscan** during apply if `enable_connector=true` (fetches host key)

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Connector apply fails host key scan | Set `connector_trusted_host_keys` in module call or retry from network with SSH egress |
| Destroy fails on bucket not empty | Ensure `force_destroy = true`; empty versioned objects |
| Cognito auth fails | Confirm `admin_password` meets policy; user exists in tfvars email |
