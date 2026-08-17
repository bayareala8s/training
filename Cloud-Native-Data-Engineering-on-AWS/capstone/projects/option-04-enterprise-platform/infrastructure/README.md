# Infrastructure – Option 4 Enterprise Data Platform

**Project key:** `cnde-cap-enterprise`  
**Tag:** `Project=capstone-option-4`

This capstone reuses the course lab stack (`scripts/lab-cycle.sh`) for S3, Glue, Step Functions, CloudWatch, and SNS. Platform-specific artifacts live in this project:

- `src/orchestration/daily_etl.asl.json` – Step Functions definition
- `monitoring/dashboard_widgets.json` – CloudWatch dashboard widgets
- `src/etl/glue_job.py` – Glue job producing KPIs + ML features

## Prerequisites

- AWS CLI configured
- Course lab Terraform available from repo root
- Python 3.10+ for local validation/curated transforms

## Deploy

```bash
# From course repo root
./scripts/lab-cycle.sh start
source ./scripts/lab-env.sh
```

Shared helper:

```bash
bash ../../_shared/deploy-aws.sh
```

Required tags:

```text
Project=capstone-option-4
Course=cloud-native-data-engineering
Environment=dev
Owner=capstone-student
```

## Wire orchestration

1. Create/update a Step Functions state machine using `src/orchestration/daily_etl.asl.json`.
2. Replace ARN placeholders (`REPLACE_WITH_*`) with lab outputs for Glue job, Lambda validators, and SNS topic.
3. Schedule with EventBridge (`cron(0 6 * * ? *)` for 06:00 UTC daily).

## Monitoring

Import widget definitions from `monitoring/dashboard_widgets.json` into a CloudWatch dashboard named `cnde-cap-enterprise-ops`.

## Upload local output

```bash
cd ..
bash scripts/run_local.sh --upload --bucket "$BUCKET"
# s3://$BUCKET/capstone/cnde-cap-enterprise/
```

## Teardown

```bash
./scripts/lab-cycle.sh stop --yes
```
