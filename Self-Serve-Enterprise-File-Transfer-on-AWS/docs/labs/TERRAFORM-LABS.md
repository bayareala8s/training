# Terraform lab environment (all weeks)

All hands-on labs use one stack: **`infra/environments/lab`**.

## Lifecycle scripts

| Script | Action |
|--------|--------|
| [`../../scripts/start_stack.sh`](../../scripts/start_stack.sh) | `terraform apply` — **provision** |
| [`../../scripts/stop_stack.sh`](../../scripts/stop_stack.sh) | `terraform destroy` — **remove all charges** |
| [`../../scripts/lab_cycle.sh`](../../scripts/lab_cycle.sh) | start → verify → optional `--destroy` |
| [`../../scripts/verify_labs.sh`](../../scripts/verify_labs.sh) | Smoke test S3, Step Functions, API |
| [`../../scripts/get_sftp_private_key.sh`](../../scripts/get_sftp_private_key.sh) | Lab 1 SFTP key |
| [`../../scripts/cognito_login.sh`](../../scripts/cognito_login.sh) | Lab 6 JWT token |

## One-time setup

```bash
cd /path/to/Course-Enterprise-File-Transfer-Automation-on-AWS
cp infra/environments/lab/terraform.tfvars.example infra/environments/lab/terraform.tfvars
# Edit admin_email and admin_password
chmod +x scripts/*.sh
```

## Start labs (after class)

```bash
./scripts/start_stack.sh --yes
```

## End labs (avoid Transfer hourly cost)

```bash
./scripts/stop_stack.sh --yes
```

## Zero overnight cost

```bash
./scripts/lab_cycle.sh --yes --destroy
```

## Outputs cheat sheet

```bash
export AWS_REGION=$(terraform -chdir=infra/environments/lab output -raw aws_region)
export BUCKET=$(terraform -chdir=infra/environments/lab output -raw landing_bucket)
export SFTP_HOST=$(terraform -chdir=infra/environments/lab output -raw transfer_server_endpoint)
export API=$(terraform -chdir=infra/environments/lab output -raw api_endpoint)
```

## Week-to-resource map

| Week | You use |
|------|---------|
| 1 | Transfer SFTP + S3 `partners/demo/inbound/` |
| 2 | KMS on buckets, access logs, IAM (review in console) |
| 3 | S3 upload triggers `baylearn-mft-lab-s3-processor` |
| 4 | Step Functions `baylearn-mft-lab-transfer-workflow` |
| 5 | Connector ID output + staging/outbound prefixes |
| 6 | Cognito + HTTP API `/v1/connections`, `/v1/jobs` |
| 7 | CloudWatch dashboard + alarms |
| 8 | Full stack + capstone |
| **9** | ECS Fargate — `large/inbound/` → worker → `large/processed/` |

### Lab 9 scripts

| Script | Purpose |
|--------|---------|
| `scripts/build_ecs_worker.sh` | Build & push Docker image to ECR |
| `scripts/demo_ecs_large_file.sh` | Upload large test file + wait for manifest |
| `scripts/run_ecs_worker.sh` | Manual `ecs run-task` |

```bash
LAB_LARGE_FILE_MB=10 ./scripts/demo_ecs_large_file.sh
```

Set `enable_ecs_worker = false` in `terraform.tfvars` to skip VPC/ECS (weeks 1–8 only).

See [`../../infra/README.md`](../../infra/README.md) for architecture detail.
