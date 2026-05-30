# Lab 3.1: Build Raw → Cleaned ETL with AWS Glue

> 📊 **Diagrams:** [Mermaid](diagram.md) · [Draw.io (lab-3.1-etl-raw-to-cleaned.drawio)](../../../../docs/diagrams/drawio/lab-3.1-etl-raw-to-cleaned.drawio) · [PNG](../../../../docs/diagrams/png/lab-3.1-etl-raw-to-cleaned.png) · [SVG](../../../../docs/diagrams/svg/lab-3.1-etl-raw-to-cleaned.svg)

**Estimated time:** 120 minutes · **Module 3**

---

## Objectives

- Deploy Glue infrastructure (IAM role, catalog database, job) with Terraform
- Upload a PySpark ETL script to S3 and configure a Glue ETL job
- Transform retail orders from Raw CSV to Cleaned Parquet
- Verify output with AWS CLI and validate record counts
- Document the cleaned-layer schema contract

---

## Prerequisites

- [Environment setup](../../../../setup/SETUP.md) complete
- Module 1 Labs 1.1 and 1.2 complete (S3 data lake + raw orders uploaded)
- Terraform 1.5+ and AWS CLI configured
- Sample data at `raw/retail/orders/year=2024/month=01/day=15/`

If raw data is missing, regenerate and upload:

```bash
cd modules/module-01-foundations/labs/lab-1.2-data-lake-zones
python scripts/generate_sample_orders.py --date 2024-01-15
export BUCKET=$(cd ../../../../infrastructure/environments/dev && terraform output -raw data_lake_bucket)
aws s3 cp sample-data/orders_2024-01-15.csv \
  s3://${BUCKET}/raw/retail/orders/year=2024/month=01/day=15/orders_2024-01-15.csv
```

---

## Architecture

```text
┌─────────────────────────────────────────────────────────────────┐
│                     S3 Data Lake (Module 1)                      │
│  raw/retail/orders/year=2024/month=01/day=15/orders_*.csv       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  AWS Glue ETL Job (glue_etl_job.py)                             │
│  - Read CSV with header                                         │
│  - Dedup, cast types, filter invalid status                     │
│  - Add processed_at, source_file                                │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  cleaned/retail/orders/year=2024/month=01/day=15/*.parquet      │
│  Format: Parquet (Snappy), Hive partitions                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Step 1: Add Glue Module to Terraform

Edit `infrastructure/environments/dev/main.tf` and add the Glue module after the data lake module:

```hcl
module "glue_etl" {
  source      = "../../modules/glue-etl"
  project     = var.project
  environment = var.environment
  student     = var.student
  aws_region  = var.aws_region
  bucket_name = module.data_lake.bucket_name
}
```

Add outputs:

```hcl
output "glue_job_name" {
  value = module.glue_etl.glue_job_name
}

output "glue_catalog_database" {
  value = module.glue_etl.glue_catalog_database
}
```

---

## Step 2: Deploy Glue Resources

```bash
cd infrastructure/environments/dev
terraform init
terraform plan
terraform apply
```

Review the plan. You should see:

- IAM role and policies for Glue
- Glue catalog database
- Glue crawler (for cleaned zone — used in Lab 3.2)
- Glue ETL job definition
- S3 object for the ETL script

Save outputs:

```bash
export BUCKET=$(terraform output -raw data_lake_bucket)
export GLUE_JOB=$(terraform output -raw glue_job_name)
export GLUE_DB=$(terraform output -raw glue_catalog_database)
```

---

## Step 3: Upload ETL Script to S3

Terraform uploads a placeholder script. Replace it with the lab script:

```bash
cd ../../../modules/module-03-glue-etl/labs/lab-3.1-etl-raw-to-cleaned

aws s3 cp scripts/glue_etl_job.py \
  s3://${BUCKET}/glue/scripts/glue_etl_job.py
```

Verify:

```bash
aws s3 ls s3://${BUCKET}/glue/scripts/
```

---

## Step 4: Run the Glue Job

Start the job with processing date parameters:

```bash
aws glue start-job-run \
  --job-name "${GLUE_JOB}" \
  --arguments '{
    "--raw_bucket": "'"${BUCKET}"'",
    "--cleaned_bucket": "'"${BUCKET}"'",
    "--dataset_path": "retail/orders",
    "--processing_date": "2024-01-15"
  }'
```

Capture the run ID from the response:

```bash
export RUN_ID=<JobRunId-from-output>
```

Monitor status (repeat until `SUCCEEDED` or `FAILED`):

```bash
aws glue get-job-run --job-name "${GLUE_JOB}" --run-id "${RUN_ID}" \
  --query 'JobRun.{State:JobRunState,Error:ErrorMessage,DPU:DPUSeconds}' \
  --output table
```

**Console alternative:** AWS Glue → ETL jobs → your job → Run job → add parameters under **Job parameters**.

---

## Step 5: Verify Cleaned Output

List Parquet files:

```bash
aws s3 ls s3://${BUCKET}/cleaned/retail/orders/ --recursive
```

Expected structure:

```text
cleaned/retail/orders/year=2024/month=01/day=15/part-00000-....snappy.parquet
```

Check file sizes (Parquet should be smaller than source CSV):

```bash
aws s3 ls s3://${BUCKET}/cleaned/retail/orders/year=2024/month=01/day=15/ --summarize
```

---

## Step 6: Validate with Athena (Optional Preview)

If Lab 3.2 crawler is not run yet, use a quick CTAS or wait for Lab 3.2. For now, confirm via Glue job logs:

```bash
aws logs filter-log-events \
  --log-group-name /aws-glue/jobs/output \
  --filter-pattern "Cleaned record count" \
  --limit 5
```

You should see approximately **1,000 cleaned records** (some may be filtered if duplicates exist in test data).

---

## Step 7: Test Idempotency

Re-run the same job for `2024-01-15`:

```bash
aws glue start-job-run \
  --job-name "${GLUE_JOB}" \
  --arguments '{
    "--raw_bucket": "'"${BUCKET}"'",
    "--cleaned_bucket": "'"${BUCKET}"'",
    "--dataset_path": "retail/orders",
    "--processing_date": "2024-01-15"
  }'
```

After success, partition file count should remain stable (dynamic overwrite replaces partition, not entire dataset).

---

## Step 8: Document Schema Contract

Create `schema-contract.md` in this lab folder:

```markdown
# Cleaned Retail Orders — Schema Contract

| Column | Type | Required | Notes |
|--------|------|----------|-------|
| order_id | string | yes | Primary key; deduplicated |
| customer_id | string | no | |
| product_category | string | no | |
| quantity | int | no | |
| unit_price | double | no | |
| total_amount | double | no | Recomputed in ETL |
| order_status | string | no | pending, shipped, delivered, cancelled |
| order_timestamp | timestamp | no | |
| region | string | no | |
| processed_at | timestamp | yes | ETL lineage |
| source_file | string | yes | S3 URI of raw input |
| year, month, day | string | yes | Hive partition keys |

## Partitioning
`s3://{bucket}/cleaned/retail/orders/year={YYYY}/month={MM}/day={DD}/`

## Idempotency
Re-run for same processing_date overwrites that partition only.
```

---

## Step 9: Lab Report

Create `LAB-REPORT.md`:

```markdown
# Lab 3.1 Report

## Resources
- Glue job: <name>
- Catalog database: <name>
- Bucket: <name>

## Job Run
- Run ID: <id>
- State: SUCCEEDED
- Raw count / Cleaned count: <from logs>

## Verification
- [ ] Parquet files under cleaned/retail/orders/year=2024/month=01/day=15/
- [ ] Job completed without ErrorMessage
- [ ] Idempotent re-run succeeded

## Screenshots
Glue job run details, S3 cleaned prefix listing.
```

---

## Deliverables

- [ ] Glue module applied via Terraform
- [ ] ETL script uploaded to `s3://{bucket}/glue/scripts/`
- [ ] Successful job run for `processing_date=2024-01-15`
- [ ] Parquet output in cleaned zone with correct partitions
- [ ] `schema-contract.md` and `LAB-REPORT.md`

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `AccessDenied` on S3 read/write | Verify Glue IAM role has `s3:GetObject` on `raw/*` and `s3:PutObject` on `cleaned/*` |
| `No records found at s3://...` | Confirm raw CSV path matches `orders_{date}.csv` under Hive partitions |
| Job fails with `AnalysisException` | Check CSV header matches expected columns from Module 1 generator |
| `DPU timeout` | Increase `number_of_workers` in Terraform or reduce data size for testing |
| Script not found | Re-upload to `glue/scripts/glue_etl_job.py`; check job script location in Terraform |
| `IllegalArgumentException` on timestamp | Verify `order_timestamp` is ISO format in source CSV |
| High `Records filtered` count | Inspect raw data for invalid `order_status` values or corrupt rows |

### View Driver Logs

```bash
# List recent log streams
aws logs describe-log-streams \
  --log-group-name /aws-glue/jobs/output \
  --order-by LastEventTime \
  --descending \
  --limit 3
```

---

## Cleanup

Keep resources for Labs 3.2 and 3.3. Destroy at end of Module 3 if not continuing:

```bash
cd infrastructure/environments/dev
terraform destroy
```

---

## What You Learned

- Glue ETL job lifecycle from script to managed Spark cluster
- Raw → Cleaned transformation with schema contracts
- Partitioned Parquet writes with dynamic overwrite
- Infrastructure as Code for Glue jobs and IAM

**Next:** [Lab 3.2 – Glue Crawlers & Data Catalog](../lab-3.2-glue-crawlers/README.md)
