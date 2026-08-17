# Lab Demo & Run Guide

**Instructor and student playbook** for all 26 hands-on labs in *Cloud-Native Data Engineering on AWS*.

Use this guide to **deploy**, **demo**, and **verify** every lab in a live AWS account.

---

## Before You Begin (one-time)

### 1. Install tools

Complete [setup/SETUP.md](../setup/SETUP.md):

- AWS CLI v2 (`aws sts get-caller-identity`)
- Terraform ≥ 1.5
- Python 3.10+ with `pip install -r requirements.txt`

### 2. Configure Terraform

```bash
cd infrastructure/environments/dev
cp terraform.tfvars.example terraform.tfvars
# Edit student name and alert_email if desired
```

### 3. Start / stop the lab environment

```bash
./scripts/lab-cycle.sh start              # deploy + seed data (labs RUNNING)
source ./scripts/lab-env.sh               # load $BUCKET, $GLUE_JOB, etc.

# When finished — zero ongoing cost:
./scripts/lab-cycle.sh stop --yes

# Check status anytime:
./scripts/lab-cycle.sh status
```

Legacy scripts (still work): `./scripts/start-labs.sh`, `./scripts/stop-labs.sh`

This deploys S3, 3 Lambdas, Glue job + crawler, quality Lambda, Step Functions, and monitoring (dashboard + SNS alarms). It also seeds sample retail orders data.

### 4. Load lab environment variables

```bash
source ./scripts/lab-env.sh
```

Prints `bucket`, `GLUE_JOB`, `SFN_ARN`, Lambda names, etc.

### 5. Verify deployment

```bash
./scripts/verify-labs.sh
```

### 6. Automated full validation (optional, ~30–40 min)

```bash
./scripts/test-all-labs.sh
```

Runs `test-modules-1-6.sh` then `test-modules-7-9.sh`, deploys if needed, tears down at end.

### 7. Tear down when finished (no ongoing cost)

```bash
./scripts/lab-cycle.sh stop --yes
```

---

## Lab quick reference

| Lab | Type | Needs `lab-cycle start` | Demo time |
|-----|------|-------------------|-----------|
| 1.1 Build S3 Data Lake | Terraform | Yes (or run lab steps) | 15 min |
| 1.2 Data Lake Zones | CLI + Python | Yes | 10 min |
| 2.1 Lambda Ingestion | Lambda invoke | Yes | 10 min |
| 2.2 EventBridge Automation | Lambda invoke | Yes | 10 min |
| 2.3 S3 Event Processing | S3 upload | Yes | 10 min |
| 3.1 Raw → Cleaned ETL | Glue job | Yes | 15 min |
| 3.2 Glue Crawlers | Crawler + Athena | Yes | 10 min |
| 3.3 ETL Optimization | Glue job (optimized) | Yes | 20 min |
| 4.1 Quality Framework | Local Python | No (local only) | 10 min |
| 4.2 Validation Automation | Lambda invoke | Yes | 15 min |
| 4.3 Quarantine Zone | S3 upload | Yes | 10 min |
| 5.1 Star Schema | Athena SQL | Yes + Glue run | 20 min |
| 5.2 Athena Optimization | Athena SQL | Yes | 15 min |
| 5.3 Cost-Efficient Queries | Athena SQL | Yes | 15 min |
| 6.1 Step Functions ETL | Step Functions | Yes | 15 min |
| 6.2 Retry & Error Branching | Update SFN ASL | Yes | 20 min |
| 6.3 SNS Failure Handling | Update SFN ASL | Yes | 15 min |
| 7.1 KMS & Bucket Policies | CLI script | Yes | 15 min |
| 7.2 IAM RBAC Data Zones | IAM + simulate | Yes | 20 min |
| 7.3 Governance Audit | Audit script | Yes + 7.1/7.2 | 15 min |
| 8.1 CloudWatch Dashboards | Console / Terraform | Yes | 10 min |
| 8.2 SNS Alerts | SNS publish | Yes | 10 min |
| 8.3 Cost Reporting | Tags + Console | Yes | 15 min |
| 9.1 ML Dataset Prep | Local Python + S3 | Optional S3 | 15 min |
| 9.2 Feature Store Pipeline | Local Python + S3 | Optional S3 | 15 min |
| 9.3 AI Data Quality | Local Python | 9.1 output | 10 min |

---

# Module 1 — Data Lake Foundations

## Lab 1.1: Build S3 Data Lake with Terraform

**What it demonstrates:** IaC deployment of an encrypted, versioned S3 data lake with medallion zones.

### Steps

```bash
cd infrastructure/environments/dev
terraform init
terraform plan
terraform apply
```

Or use the course script (includes seed data):

```bash
./scripts/start-labs.sh
source ./scripts/lab-env.sh
```

### Verify

```bash
aws s3api get-bucket-versioning --bucket "$BUCKET"
aws s3api get-public-access-block --bucket "$BUCKET"
aws s3 ls "s3://${BUCKET}/"
```

Expected: versioning `Enabled`, all public access blocked, zones `raw/`, `cleaned/`, `curated/`, `quarantine/`, `metadata/`.

### Demo tip

Show Terraform outputs and the S3 console → bucket → Properties (encryption, versioning, lifecycle).

### Console

S3 → `cnde-dev-datalake-{account-id}` → Permissions / Management

---

## Lab 1.2: Data Lake Zones

**What it demonstrates:** Medallion layout, Hive-style partitioning, metadata manifests.

### Steps

```bash
source ./scripts/lab-env.sh
cd "$LAB12"

# Generate and upload sample orders (if not already seeded by start-labs)
python3 scripts/generate_sample_orders.py --count 1000 --date 2024-01-15
aws s3 cp sample-data/orders_2024-01-15.csv \
  "s3://${BUCKET}/raw/retail/orders/year=2024/month=01/day=15/orders_2024-01-15.csv"

"$PYTHON" scripts/create_manifest.py \
  --bucket "$BUCKET" --dataset retail/orders \
  --source-file sample-data/orders_2024-01-15.csv

"$PYTHON" scripts/validate_zones.py --bucket "$BUCKET"
```

### Verify

```bash
aws s3 ls "s3://${BUCKET}/raw/retail/orders/" --recursive | head
aws s3 ls "s3://${BUCKET}/metadata/" --recursive
```

### Demo tip

Explain partition path `year=2024/month=01/day=15/` and why Athena/Glue use it for pruning.

---

# Module 2 — Data Ingestion

## Lab 2.1: Lambda Ingestion

**What it demonstrates:** JSON records → Lambda → idempotent S3 raw keys.

### Steps

```bash
source ./scripts/lab-env.sh

aws lambda invoke \
  --function-name "$FN_FILE" \
  --payload '{"records":[{"record_id":"demo-001","amount":99.50,"currency":"USD"}]}' \
  --cli-binary-format raw-in-base64-out /tmp/lab21.json

cat /tmp/lab21.json
aws s3 ls "s3://${BUCKET}/raw/" --recursive | tail -5
```

### Verify

Response contains `"ingested": 1`. New object under `raw/lambda-ingest/`.

### Demo tip

Invoke twice with same `record_id` to discuss idempotency.

---

## Lab 2.2: EventBridge Automation

**What it demonstrates:** Scheduled / incremental ingestion pattern (manual invoke in dev).

### Steps

```bash
source ./scripts/lab-env.sh

aws lambda invoke \
  --function-name "$FN_SCHED" \
  --payload '{}' \
  --cli-binary-format raw-in-base64-out /tmp/lab22.json

cat /tmp/lab22.json
```

### Verify

Lambda returns success; check CloudWatch Logs: `/aws/lambda/${FN_SCHED}`.

### Demo tip

Note schedules are **disabled** by default (`enable_schedules=false`). Show EventBridge rule exists but is disabled.

---

## Lab 2.3: S3 Event Processing

**What it demonstrates:** `incoming/` upload triggers promotion to `raw/` or `quarantine/`.

### Steps

```bash
source ./scripts/lab-env.sh

echo '{"record_id":"demo-s3-001","amount":25.00}' > /tmp/incoming.json
aws s3 cp /tmp/incoming.json "s3://${BUCKET}/incoming/demo-s3-001.json"
sleep 20
aws s3 ls "s3://${BUCKET}/raw/" --recursive | grep demo || true
aws s3 ls "s3://${BUCKET}/quarantine/" --recursive | grep demo || true
```

### Verify

File appears under `raw/` (valid JSON) or `quarantine/` (invalid).

### Fallback (if S3 event is slow)

```bash
aws lambda invoke --function-name "$FN_S3" \
  --payload '{"Records":[{"eventSource":"aws:s3","s3":{"bucket":{"name":"'"$BUCKET"'"},"object":{"key":"incoming/demo-s3-001.json"}}}]}' \
  --cli-binary-format raw-in-base64-out /tmp/lab23.json
cat /tmp/lab23.json
```

---

# Module 3 — Glue ETL

## Lab 3.1: Raw → Cleaned ETL

**What it demonstrates:** Glue PySpark transforms CSV → Parquet in `cleaned/`.

### Steps

```bash
source ./scripts/lab-env.sh

RUN_ID=$(aws glue start-job-run \
  --job-name "$GLUE_JOB" \
  --arguments '{"--processing_date":"2024-01-15","--dataset_path":"retail/orders"}' \
  --query 'JobRunId' --output text)

echo "Run ID: $RUN_ID"
# Wait ~3–8 minutes
aws glue get-job-run --job-name "$GLUE_JOB" --run-id "$RUN_ID" \
  --query 'JobRun.JobRunState' --output text
```

### Verify

```bash
aws s3 ls "s3://${BUCKET}/cleaned/retail/orders/" --recursive | grep parquet
```

State = `SUCCEEDED`.

### Demo tip

Open Glue console → Jobs → Run details → DPU seconds.

---

## Lab 3.2: Glue Crawlers & Catalog

**What it demonstrates:** Crawler discovers schema → Glue Data Catalog → Athena.

### Steps

```bash
source ./scripts/lab-env.sh

aws glue start-crawler --name "$CRAWLER"
# Wait until READY (~2–5 min)
aws glue get-crawler --name "$CRAWLER" --query 'Crawler.State' --output text
aws glue get-tables --database-name "$GLUE_DB" --query 'TableList[].Name' --output table
```

### Verify

At least one table in `cnde_dev_datalake` database.

### Athena smoke query

```bash
aws athena start-query-execution \
  --query-string "SELECT COUNT(*) FROM ${GLUE_DB}.orders_cleaned LIMIT 10" \
  --query-execution-context "Database=${GLUE_DB}" \
  --result-configuration "OutputLocation=${ATHENA_RESULTS}"
```

---

## Lab 3.3: ETL Optimization

**What it demonstrates:** Baseline vs optimized Glue job (partitioning, coalesce, file sizes).

### Steps

```bash
source ./scripts/lab-env.sh

# Baseline (same as 3.1) — record ExecutionTime and DPUSeconds
aws glue start-job-run --job-name "$GLUE_JOB" \
  --arguments '{"--processing_date":"2024-01-15","--dataset_path":"retail/orders"}'

# Review optimized script (students compare with lab-3.1 script)
code modules/module-03-glue-etl/labs/lab-3.3-etl-optimization/scripts/glue_etl_job_optimized.py
```

### Verify

Document before/after metrics in `optimization-baseline.md` (per lab README). Compare Parquet file count and sizes:

```bash
aws s3 ls "s3://${BUCKET}/cleaned/retail/orders/" --recursive --summarize
```

### Demo tip

Show Athena `EXPLAIN` or bytes scanned difference after optimization (ties to Lab 5.2).

---

# Module 4 — Data Quality

## Lab 4.1: Quality Framework

**What it demonstrates:** Rule engine validates records locally; routes pass/quarantine.

### Steps

```bash
source ./scripts/lab-env.sh
cd "$LAB41"

"$PYTHON" src/quality_runner.py \
  --rules rules/orders_rules.json \
  --input sample-data/orders_sample.json \
  --output-dir /tmp/cnde-quality

cat /tmp/cnde-quality/quality_report.json
```

### Verify

`quality_report.json` shows pass/quarantine counts. No AWS required.

---

## Lab 4.2: Validation Automation

**What it demonstrates:** Quality checks integrated into deployed Lambda (Terraform module).

### Steps

```bash
source ./scripts/lab-env.sh

aws lambda invoke \
  --function-name "$QV_LAMBDA" \
  --payload '{"dataset":"retail/orders","processing_date":"2024-01-15"}' \
  --cli-binary-format raw-in-base64-out /tmp/lab42.json

cat /tmp/lab42.json
```

### Verify

Lambda returns validation result. Check CloudWatch Logs: `/aws/lambda/${QV_LAMBDA}`.

### Demo tip

Connect to Step Functions pipeline (Lab 6.1) — same validation Lambda is orchestrated there.

---

## Lab 4.3: Quarantine Zone

**What it demonstrates:** Bad records isolated under `quarantine/` for steward review.

### Steps

```bash
source ./scripts/lab-env.sh

aws s3 cp /tmp/cnde-quality/quarantined_records.json \
  "s3://${BUCKET}/quarantine/retail/orders/demo/quarantined_records.json"

aws s3 ls "s3://${BUCKET}/quarantine/" --recursive
```

### Verify

Object exists in quarantine prefix. Discuss replay workflow from lab README.

---

# Module 5 — Modeling & Analytics

## Lab 5.1: Star Schema

**What it demonstrates:** dim/fact tables in Athena over curated zone.

### Prerequisites

Run Lab 3.1 first so cleaned data exists.

### Steps

```bash
source ./scripts/lab-env.sh
cd "$LAB51/scripts"

# Run SQL scripts in order (Athena console or CLI)
for f in 01_create_database.sql 02_create_dim_customer.sql 03_create_dim_product.sql \
         04_create_fact_orders.sql 05_load_dimensions.sql 06_load_fact_orders.sql; do
  echo "=== $f ==="
  SQL=$(sed "s/\${DATABASE}/${GLUE_DB}/g; s/\${BUCKET}/${BUCKET}/g" "$f")
  aws athena start-query-execution \
    --query-string "$SQL" \
    --query-execution-context "Database=${GLUE_DB}" \
    --result-configuration "OutputLocation=${ATHENA_RESULTS}"
done
```

### Verify

```bash
aws athena start-query-execution \
  --query-string "SELECT COUNT(*) FROM ${GLUE_DB}.fact_orders" \
  --query-execution-context "Database=${GLUE_DB}" \
  --result-configuration "OutputLocation=${ATHENA_RESULTS}"
```

### Demo tip

Draw star schema on whiteboard; run `07_validation_queries.sql`.

---

## Lab 5.2: Athena Optimization

**What it demonstrates:** Partition pruning, column projection, bytes scanned.

### Steps

```bash
source ./scripts/lab-env.sh
cd modules/module-05-modeling-analytics/labs/lab-5.2-athena-optimization/scripts

# Run before_queries.sql then after_queries.sql in Athena
# Compare Data scanned in query history
cat before_queries.sql after_queries.sql
```

### Verify

"After" queries scan fewer bytes (check Athena console → History → Data scanned).

---

## Lab 5.3: Cost-Efficient Queries

**What it demonstrates:** Summary tables and analyst views reduce scan cost.

### Steps

```bash
source ./scripts/lab-env.sh
cd "$LAB53/scripts"

# Create summary table and views (run in Athena)
cat create_summary_table.sql create_analyst_views.sql dashboard_queries.sql
```

### Verify

Compare `SELECT` on `fact_orders` vs `daily_revenue_summary` — summary should scan less data.

---

# Module 6 — Orchestration

## Lab 6.1: Step Functions ETL

**What it demonstrates:** Multi-stage pipeline: Glue → quality validation → success.

### Steps

```bash
source ./scripts/lab-env.sh

EXEC_ARN=$(aws stepfunctions start-execution \
  --state-machine-arn "$SFN_ARN" \
  --name "demo-$(date +%s)" \
  --input '{"processing_date":"2024-01-15","dataset":"retail/orders","triggered_by":"demo"}' \
  --query 'executionArn' --output text)

echo "$EXEC_ARN"
# Wait ~5–10 min
aws stepfunctions describe-execution --execution-arn "$EXEC_ARN" \
  --query '{status:status,output:output}' --output json
```

### Verify

Status = `SUCCEEDED`. View graph in Step Functions console.

---

## Lab 6.2: Retry & Error Branching

**What it demonstrates:** Retry policies, Catch states, degraded-quality warning path.

### Steps

```bash
source ./scripts/lab-env.sh
cd modules/module-06-orchestration/labs/lab-6.2-retry-error-branching

mkdir -p build
QV_ARN=$(aws lambda get-function --function-name "$QV_LAMBDA" --query 'Configuration.FunctionArn' --output text)

sed -e "s|\${GLUE_JOB_NAME}|${GLUE_JOB}|g" \
    -e "s|\${VALIDATION_LAMBDA_ARN}|${QV_ARN}|g" \
    src/daily_etl_with_retry.asl.json > build/resolved.asl.json

aws stepfunctions update-state-machine \
  --state-machine-arn "$SFN_ARN" \
  --definition file://build/resolved.asl.json

# Start execution and observe retry branches in console
aws stepfunctions start-execution \
  --state-machine-arn "$SFN_ARN" \
  --name "demo-retry-$(date +%s)" \
  --input '{"processing_date":"2024-01-15","dataset":"retail/orders"}'
```

### Verify

Execution graph shows Retry/Catch states. Revert to Lab 6.1 definition if needed (re-apply Terraform).

---

## Lab 6.3: SNS Failure Handling

**What it demonstrates:** Failed pipeline steps publish to SNS critical topic.

### Steps

```bash
source ./scripts/lab-env.sh
cd modules/module-06-orchestration/labs/lab-6.3-sns-failure-handling

mkdir -p build
QV_ARN=$(aws lambda get-function --function-name "$QV_LAMBDA" --query 'Configuration.FunctionArn' --output text)

sed -e "s|\${GLUE_JOB_NAME}|${GLUE_JOB}|g" \
    -e "s|\${VALIDATION_LAMBDA_ARN}|${QV_ARN}|g" \
    -e "s|\${SNS_TOPIC_ARN}|${SNS_CRITICAL}|g" \
    src/daily_etl_with_sns.asl.json > build/resolved.asl.json

aws stepfunctions update-state-machine \
  --state-machine-arn "$SFN_ARN" \
  --definition file://build/resolved.asl.json
```

### Verify

Trigger a failure (invalid input) and confirm SNS message. Check email subscription if confirmed.

```bash
aws sns publish --topic-arn "$SNS_CRITICAL" --message "CNDE demo alert test"
```

---

# Module 7 — Security & Governance

## Lab 7.1: KMS & Bucket Policies

**What it demonstrates:** SSE-KMS default encryption on the data lake.

### Steps

```bash
source ./scripts/lab-env.sh
export BUCKET KMS_ALIAS=alias/cnde-dev-datalake-key
cd "$LAB71"
chmod +x scripts/apply_encryption.sh
./scripts/apply_encryption.sh
```

### Verify

```bash
aws s3api get-bucket-encryption --bucket "$BUCKET"
aws kms describe-key --key-id "$KMS_ALIAS"
```

SSE algorithm = `aws:kms`.

---

## Lab 7.2: IAM RBAC Data Zones

**What it demonstrates:** Least-privilege roles per medallion zone.

### Steps

```bash
source ./scripts/lab-env.sh
cd "$LAB72"

ASSUME_DOC='{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"AWS":["arn:aws:iam::'"$ACCOUNT_ID"':root","'"$CALLER_ARN"'"]},"Action":"sts:AssumeRole"}]}'

for ROLE in cnde-dev-analyst-curated cnde-dev-engineer-pipeline cnde-dev-steward-quarantine; do
  aws iam create-role --role-name "$ROLE" --assume-role-policy-document "$ASSUME_DOC" 2>/dev/null || true
done

for PAIR in "cnde-dev-analyst-curated:analyst-curated-read" \
            "cnde-dev-engineer-pipeline:engineer-pipeline-write" \
            "cnde-dev-steward-quarantine:steward-quarantine"; do
  ROLE="${PAIR%%:*}"; POLICY="${PAIR##*:}"
  sed "s/BUCKET_NAME/${BUCKET}/g" "policies/${POLICY}.json" > "/tmp/${POLICY}.json"
  aws iam put-role-policy --role-name "$ROLE" --policy-name "$POLICY" \
    --policy-document "file:///tmp/${POLICY}.json"
done
```

### Verify (policy simulation)

```bash
aws iam simulate-principal-policy \
  --policy-source-arn "arn:aws:iam::${ACCOUNT_ID}:role/cnde-dev-analyst-curated" \
  --action-names s3:ListBucket \
  --resource-arns "arn:aws:s3:::${BUCKET}" \
  --query 'EvaluationResults[0].EvalDecision'
```

Expected: `explicitDeny` for raw access patterns.

---

## Lab 7.3: Governance Audit

**What it demonstrates:** Automated evidence collection for compliance report.

### Steps

```bash
source ./scripts/lab-env.sh
export BUCKET REPORT_DIR=/tmp/cnde-audit
cd "$LAB73"
./scripts/run_audit_checks.sh
ls -la "$REPORT_DIR"
```

### Verify

Review `s3-encryption.txt`, `iam-roles.txt`, `cloudtrail.txt`. Complete `templates/audit-report-template.md`.

---

# Module 8 — Monitoring & Operations

## Lab 8.1: CloudWatch Dashboards

**What it demonstrates:** ETL pipeline observability (Glue, Lambda, quality metrics).

### Steps

```bash
source ./scripts/lab-env.sh

aws cloudwatch get-dashboard --dashboard-name "$DASHBOARD" \
  --query 'DashboardBody' --output text | head -c 500

# Publish sample quality metric for widgets
aws cloudwatch put-metric-data \
  --namespace "CNDE/DataQuality" \
  --metric-data "MetricName=ValidationPassRate,Value=99.5,Unit=Percent,Dimensions=[{Name=Dataset,Value=retail/orders},{Name=Environment,Value=dev}]"
```

### Verify

Console → CloudWatch → Dashboards → `cnde-dev-etl-pipeline`.

---

## Lab 8.2: SNS Alerts

**What it demonstrates:** Alarms route to SNS critical/warning topics.

### Steps

```bash
source ./scripts/lab-env.sh

aws sns publish --topic-arn "$SNS_CRITICAL" \
  --message "CNDE Lab 8.2 demo alert $(date -u +%Y-%m-%dT%H:%M:%SZ)"

aws cloudwatch describe-alarms --alarm-name-prefix cnde-dev- \
  --query 'MetricAlarms[].{Name:AlarmName,State:StateValue}' --output table
```

### Verify

Confirm SNS email subscription (if configured in `terraform.tfvars`). Alarms show `OK` or `INSUFFICIENT_DATA`.

---

## Lab 8.3: Cost Reporting

**What it demonstrates:** Cost allocation tags for FinOps reporting.

### Steps

```bash
source ./scripts/lab-env.sh

aws s3api get-bucket-tagging --bucket "$BUCKET"
```

### Verify

Tags present: `Project`, `Environment`, `Course`, `ManagedBy`, `Student`.

### Console demo

Billing → Cost Allocation Tags → activate tags → Cost Explorer → filter by `Project=cnde`.

---

# Module 9 — AI/ML Data Engineering

## Lab 9.1: ML Dataset Preparation

**What it demonstrates:** Point-in-time features, temporal train/val/test splits.

### Steps

```bash
source ./scripts/lab-env.sh
cd "$LAB91"
rm -rf output

"$PYTHON" src/prepare_ml_dataset.py --output output
ls -la output/
cat output/dataset_manifest.json
```

### Optional S3 upload

```bash
aws s3 sync output/ "s3://${BUCKET}/ml/datasets/lab91/"
```

### Verify

`train.parquet`, `validation.parquet`, `test.parquet` exist with row counts > 0.

---

## Lab 9.2: Feature Store Pipeline

**What it demonstrates:** Offline feature store pattern (maps to SageMaker Feature Store).

### Steps

```bash
source ./scripts/lab-env.sh
cd "$LAB92"
rm -rf output

"$PYTHON" src/feature_pipeline.py --output output/ml/features
cat output/ml/features/pipeline_manifest.json
find output/ml/features -name '*.parquet'
```

### Optional S3 upload

```bash
aws s3 sync output/ml/features/ "s3://${BUCKET}/ml/features/"
```

### Verify

Two feature groups: `customer_behavior`, `product_catalog`.

---

## Lab 9.3: AI Data Quality

**What it demonstrates:** ML-specific checks (PSI drift, label balance, leakage).

### Steps

```bash
source ./scripts/lab-env.sh
cd "$LAB93"
rm -rf output

"$PYTHON" src/ai_quality_validator.py \
  --data-dir "${LAB91}/output" \
  --output output

cat output/ai_quality_report.json
```

### Verify

`overall_passed: true` in report.

---

# Instructor demo flow (recommended order)

For a **single 2-hour live demo** covering the full platform:

| Order | Lab | Action | Time |
|-------|-----|--------|------|
| 1 | Setup | `./scripts/lab-cycle.sh start` + `source lab-env.sh` | 10 min |
| 2 | 1.1/1.2 | Show S3 zones + sample data | 5 min |
| 3 | 2.1 | Lambda ingest one record | 5 min |
| 4 | 3.1 | Start Glue job (runs in background) | 5 min |
| 5 | 4.1 | Local quality runner | 5 min |
| 6 | 3.2 | Start crawler while Glue runs | 5 min |
| 7 | 5.1 | Athena COUNT on cleaned table | 10 min |
| 8 | 6.1 | Start Step Functions execution | 5 min |
| 9 | 8.1 | Open CloudWatch dashboard | 5 min |
| 10 | 7.1 | Apply KMS encryption | 10 min |
| 11 | 9.1–9.3 | Run ML pipeline locally | 15 min |
| 12 | — | `./scripts/lab-cycle.sh stop --yes` | 5 min |

---

# Troubleshooting

| Issue | Fix |
|-------|-----|
| `BUCKET` empty after `lab-env.sh` | Run `./scripts/lab-cycle.sh start` first |
| Glue job fails | Check `/aws-glue/jobs/error` logs; verify raw CSV exists for `2024-01-15` |
| Athena table not found | Run crawler (Lab 3.2) or `MSCK REPAIR TABLE` |
| Step Functions fails | Check execution history; ensure Glue job name matches |
| `sts:AssumeRole` denied | Use `iam simulate-principal-policy` (Lab 7.2) or add your ARN to trust policy |
| Module 9 empty splits | Re-run Lab 9.1 after latest `prepare_ml_dataset.py` fix |
| Proxy errors | Scripts unset `HTTP_PROXY` automatically |

---

# Related docs

- [COURSE-INDEX.md](COURSE-INDEX.md) — full content map
- [diagrams/README.md](diagrams/README.md) — architecture diagrams
- [scripts/README.md](../scripts/README.md) — deploy/teardown scripts
- [INSTRUCTOR-GUIDE.md](INSTRUCTOR-GUIDE.md) — teaching notes
