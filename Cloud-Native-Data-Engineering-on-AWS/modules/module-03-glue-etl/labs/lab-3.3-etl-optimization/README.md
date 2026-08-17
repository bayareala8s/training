# Lab 3.3: ETL Optimization — Partitioning and Parquet

> 📊 **Diagrams:** [Mermaid](diagram.md) · [Draw.io (lab-3.3-etl-optimization.drawio)](../../../../docs/diagrams/drawio/lab-3.3-etl-optimization.drawio) · [PNG](../../../../docs/diagrams/png/lab-3.3-etl-optimization.png) · [SVG](../../../../docs/diagrams/svg/lab-3.3-etl-optimization.svg)

**Estimated time:** 90 minutes · **Module 3**

---

## Objectives

- Measure Glue job runtime and DPU consumption before and after optimization
- Apply partition pruning and column pruning in Athena queries
- Optimize Parquet file sizes to avoid the "small files problem"
- Tune Glue worker count and Spark settings for cost/performance balance
- Document an optimization playbook for production ETL

---

## Prerequisites

- Labs 3.1 and 3.2 complete
- Cleaned Parquet data for at least one partition (`2024-01-15`)
- Familiarity with Athena query statistics (data scanned)

---


## Platform Setup

From the **repository root**, start the shared lab environment (once per session):

```bash
./scripts/lab-cycle.sh start
source ./scripts/lab-env.sh
```

Stop when finished: `./scripts/lab-cycle.sh stop --yes` (avoids ongoing AWS charges).

---


## Architecture: Optimization Focus

```text
                    BEFORE                          AFTER
         ┌─────────────────────┐        ┌─────────────────────┐
         │ Many tiny Parquet   │        │ ~128–256 MB files   │
         │ files per partition │   →    │ coalesced per part. │
         │ No partition filter │        │ Predicate pushdown  │
         │ G.1X × 2 workers    │        │ Right-sized workers │
         └─────────────────────┘        └─────────────────────┘
                    │                              │
                    └──────────┬───────────────────┘
                               ▼
                    Lower DPU-seconds + lower Athena scan cost
```

---

## Step 1: Baseline Metrics

Run the existing Glue job and record baseline:

```bash
cd infrastructure/environments/dev
export BUCKET=$(terraform output -raw data_lake_bucket)
export GLUE_JOB=$(terraform output -raw glue_job_name)

aws glue start-job-run \
  --job-name "${GLUE_JOB}" \
  --arguments '{
    "--raw_bucket": "'"${BUCKET}"'",
    "--cleaned_bucket": "'"${BUCKET}"'",
    "--dataset_path": "retail/orders",
    "--processing_date": "2024-01-15"
  }'
```

After completion, capture metrics:

```bash
export RUN_ID=<JobRunId>

aws glue get-job-run --job-name "${GLUE_JOB}" --run-id "${RUN_ID}" \
  --query 'JobRun.{State:JobRunState,ExecutionTime:ExecutionTime,DPUSeconds:DPUSeconds,WorkerType:WorkerType,NumberOfWorkers:NumberOfWorkers}' \
  --output table
```

Record in `optimization-baseline.md`:

- Execution time (seconds)
- DPU seconds
- Number of output files in partition
- Total output size (bytes)

```bash
aws s3 ls s3://${BUCKET}/cleaned/retail/orders/year=2024/month=01/day=15/ --recursive --summarize
```

---

## Step 2: Generate Multi-Day Dataset

Optimization is more meaningful with multiple partitions. Generate and load three days:

```bash
cd modules/module-01-foundations/labs/lab-1.2-data-lake-zones

for DATE in 2024-01-17 2024-01-18 2024-01-19; do
  python scripts/generate_sample_orders.py --date ${DATE} --count 2000
  YEAR=$(echo $DATE | cut -d- -f1)
  MONTH=$(echo $DATE | cut -d- -f2)
  DAY=$(echo $DATE | cut -d- -f3)
  aws s3 cp sample-data/orders_${DATE}.csv \
    s3://${BUCKET}/raw/retail/orders/year=${YEAR}/month=${MONTH}/day=${DAY}/orders_${DATE}.csv
done
```

Run ETL for each date:

```bash
for DATE in 2024-01-17 2024-01-18 2024-01-19; do
  aws glue start-job-run \
    --job-name "${GLUE_JOB}" \
    --arguments '{
      "--raw_bucket": "'"${BUCKET}"'",
      "--cleaned_bucket": "'"${BUCKET}"'",
      "--dataset_path": "retail/orders",
      "--processing_date": "'"${DATE}"'"
    }'
  echo "Started job for ${DATE}"
  sleep 30
done
```

Wait for all runs to succeed before continuing.

---

## Step 3: Add File Coalescing to ETL Script

Copy the lab script and add optimization before write. Edit `scripts/glue_etl_job_optimized.py` (create as a copy):

Key changes to apply in `write_cleaned_parquet`:

```python
def write_cleaned_parquet(df: DataFrame, output_base: str, target_files: int = 1) -> None:
    spark = df.sparkSession
    spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
    spark.conf.set("spark.sql.parquet.compression.codec", "snappy")

    # Coalesce to reduce small files (tune target_files per partition volume)
    df_out = df.coalesce(target_files)

    (
        df_out.write.mode("overwrite")
        .option("compression", "snappy")
        .partitionBy("year", "month", "day")
        .parquet(output_base)
    )
```

Upload optimized script:

```bash
cd modules/module-03-glue-etl/labs/lab-3.3-etl-optimization

# Copy from lab 3.1 and apply changes, or use provided optimized variant
aws s3 cp scripts/glue_etl_job_optimized.py \
  s3://${BUCKET}/glue/scripts/glue_etl_job.py
```

Update Terraform job `script_location` if using a separate object key, or overwrite the existing script path.

Re-run ETL for one partition and compare file count:

```bash
# After job succeeds
aws s3 ls s3://${BUCKET}/cleaned/retail/orders/year=2024/month=01/day=17/ --recursive
```

**Goal:** Fewer, larger Parquet files per partition.

---

## Step 4: Athena — Partition vs Full Scan

Run these queries in Athena and record **Data scanned**:

```sql
-- A: Full table scan (avoid in production)
SELECT COUNT(*) FROM cnde_dev_datalake.cleaned_retail_orders;

-- B: Partition filter (preferred)
SELECT COUNT(*) FROM cnde_dev_datalake.cleaned_retail_orders
WHERE year = '2024' AND month = '01' AND day = '17';

-- C: Column pruning — select only needed columns
SELECT order_status, COUNT(*)
FROM cnde_dev_datalake.cleaned_retail_orders
WHERE year = '2024' AND month = '01' AND day = '17'
GROUP BY order_status;
```

Create `athena-scan-comparison.md`:

| Query | Data Scanned | Runtime | Notes |
|-------|--------------|---------|-------|
| A | | | |
| B | | | |
| C | | | |

Query B should scan dramatically less than Query A when multiple partitions exist.

---

## Step 5: Tune Glue Workers

In `infrastructure/modules/glue-etl/main.tf`, adjust worker settings:

```hcl
number_of_workers = 3   # try 2 vs 5 and compare DPUSeconds
worker_type       = "G.1X"
```

Apply and re-run the same partition:

```bash
cd infrastructure/environments/dev
terraform apply
# Re-run job for 2024-01-18
```

**Rule of thumb:** More workers help large shuffles; for small lab data, **2 G.1X workers** is often sufficient. Over-provisioning wastes DPU-seconds.

Document findings in `worker-tuning.md`.

---

## Step 6: Spark Configuration Experiments

Add these `--conf` settings via Glue job default arguments (Terraform or console):

| Spark Conf | Purpose |
|------------|---------|
| `spark.sql.adaptive.enabled=true` | AQE optimizes shuffle partitions at runtime |
| `spark.sql.adaptive.coalescePartitions.enabled=true` | Merge small shuffle partitions |
| `spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version=2` | Faster S3 commits |

Example CLI override (if supported by your job config):

```bash
aws glue start-job-run \
  --job-name "${GLUE_JOB}" \
  --arguments '{
    "--raw_bucket": "'"${BUCKET}"'",
    "--cleaned_bucket": "'"${BUCKET}"'",
    "--dataset_path": "retail/orders",
    "--processing_date": "2024-01-19",
    "--conf": "spark.sql.adaptive.enabled=true"
  }'
```

Compare `ExecutionTime` and `DPUSeconds` to Step 1 baseline.

---

## Step 7: Compaction Strategy (Conceptual + Optional)

For production lakes, schedule periodic **compaction jobs** that:

1. Read all files in a partition
2. Coalesce to target file size (~128–256 MB)
3. Overwrite partition atomically

Optional exercise — compact one partition with a one-off Glue Python shell or second Spark job. Document when you'd use:

- **Inline coalesce** (this lab) vs
- **Async compaction** (scheduled, decoupled from ingest)

---

## Step 8: Optimization Playbook

Create `OPTIMIZATION-PLAYBOOK.md`:

```markdown
# ETL Optimization Playbook — Retail Orders

## Storage
- [ ] Parquet + Snappy in cleaned zone
- [ ] Hive partitions: year, month, day
- [ ] Target 1–N files per partition based on volume (N tuned by data size)

## Glue Job
- [ ] Dynamic partition overwrite enabled
- [ ] Worker type: G.1X for dev; scale to G.2X if shuffle-heavy
- [ ] Worker count: start at 2, increase if runtime > SLA
- [ ] AQE enabled for adaptive coalesce

## Athena / Consumers
- [ ] Always filter on partition columns
- [ ] Select only required columns
- [ ] Use MSCK REPAIR or crawler schedule for new partitions

## Monitoring
- [ ] CloudWatch alarm on job failure
- [ ] Track DPUSeconds trend week over week
- [ ] Alert on partition with >100 small files

## Baseline vs Optimized
| Metric | Before | After | Change |
|--------|--------|-------|--------|
| DPUSeconds | | | |
| Files per partition | | | |
| Athena scan (Query B) | | | |
```

---

## Deliverables

- [ ] Baseline and optimized metrics documented
- [ ] Multi-day partitions loaded and processed
- [ ] Coalescing applied; file count reduced
- [ ] Athena scan comparison (partition filter vs full scan)
- [ ] Worker tuning notes
- [ ] `OPTIMIZATION-PLAYBOOK.md`

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Coalesce causes OOM | Increase workers or use `repartition` with fewer partitions carefully |
| No improvement in DPUSeconds | Dataset too small to benefit; use larger sample or more days |
| Athena still scans full table | Verify partition columns in WHERE clause; run `MSCK REPAIR TABLE` |
| More files after rerun | Check dynamic overwrite mode; ensure same partition keys in DataFrame |
| S3 slow commits | Enable mapreduce fileoutputcommitter v2 |
| Optimized script not picked up | Confirm S3 upload path matches Glue job script location |

---

## Cleanup

After Module 3 assignment submission, destroy lab resources if not needed:

```bash
cd infrastructure/environments/dev
terraform destroy
```

---

## What You Learned

- Measuring and improving Glue job cost via DPU-seconds
- Parquet layout and small-file mitigation
- Partition and column pruning for Athena
- Documented optimization playbook for production handoff

**Next:** [Assignment 3 – Healthcare ETL Design](../../assignments/assignment-03.md)
