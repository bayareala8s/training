# Week 3 Lecture: AWS Glue ETL Engineering

**Duration:** 2 hours · **Module 3**

---

## Learning Objectives

By the end of this lecture you will:

1. Explain how AWS Glue Crawlers discover schema and register tables in the Data Catalog
2. Develop Glue ETL jobs using PySpark and the Glue libraries API
3. Design Raw → Cleaned transformations aligned with medallion architecture
4. Handle schema evolution safely in production pipelines
5. Apply partitioning, columnar formats, and job tuning to optimize cost and performance

---

## 1. AWS Glue in the Data Platform

AWS Glue is a **managed serverless ETL service** built on Apache Spark. In our course architecture, Glue sits between the S3 data lake zones and downstream analytics (Athena, QuickSight, ML).

```text
┌──────────────┐     ┌─────────────────┐     ┌──────────────────┐
│  S3 Raw      │────▶│  Glue ETL Job   │────▶│  S3 Cleaned      │
│  (CSV, JSON) │     │  (PySpark)      │     │  (Parquet)       │
└──────────────┘     └────────┬────────┘     └────────┬─────────┘
                              │                        │
                              ▼                        ▼
                     ┌─────────────────┐     ┌──────────────────┐
                     │ Glue Crawler    │     │ Glue Data Catalog│
                     │ (schema infer)  │     │ (Hive tables)    │
                     └─────────────────┘     └────────┬─────────┘
                                                      │
                                                      ▼
                                              ┌──────────────────┐
                                              │ Amazon Athena    │
                                              │ (SQL queries)    │
                                              └──────────────────┘
```

### Glue Components

| Component | Purpose |
|-----------|---------|
| **Glue Data Catalog** | Central metadata store (databases, tables, partitions) |
| **Glue Crawler** | Scans S3 and infers schema; creates/updates catalog tables |
| **Glue ETL Job** | Runs PySpark or Scala scripts on managed Spark clusters |
| **Glue Studio** | Visual ETL designer (generates code; useful for prototyping) |
| **Glue Connections** | JDBC/VPC connectivity for databases (Module 5+) |

Glue is **pay-per-use**: DPU-hours for jobs, crawler runs charged per crawl. For labs, use `G.1X` workers and small datasets to stay within budget.

---

## 2. Glue Data Catalog

The Data Catalog is a **Hive Metastore-compatible** metadata layer. Athena, Redshift Spectrum, and EMR all read from it.

### Databases and Tables

- **Database:** Logical namespace (e.g., `cnde_dev_datalake`)
- **Table:** Points to S3 location + schema + partition keys
- **Partition:** Subdirectory metadata (`year=2024/month=01/day=15`)

Example table definition (conceptual):

```sql
-- Queried in Athena after crawler or manual DDL
SELECT order_id, total_amount, order_status
FROM cnde_dev_datalake.cleaned_retail_orders
WHERE year = '2024' AND month = '01' AND day = '15'
LIMIT 10;
```

### Catalog-First Design

**Anti-pattern:** Hard-code S3 paths in every script and dashboard.

**Best practice:** Jobs write to known prefixes; crawlers (or the job itself via `sink`) register tables. Consumers query by **table name**, not path.

Benefits:

- Schema discovery for analysts
- Partition pruning in Athena
- Lineage and governance hooks (Lake Formation, Module 7)

---

## 3. Glue Crawlers

Crawlers **automatically classify** data in S3 and populate the Data Catalog.

### How a Crawler Works

1. Reads sample files from the target S3 path(s)
2. Infers column names and types (with classifiers for JSON, CSV, Parquet, etc.)
3. Detects partition keys from `key=value` path segments
4. Creates or updates a table; adds new partitions on subsequent runs

### When to Use Crawlers vs Job-Registered Tables

| Approach | Best For |
|----------|----------|
| **Crawler** | Exploratory zones, unknown schemas, many file drops |
| **Job `getSink` / DDL** | Stable cleaned/curated schemas you control explicitly |
| **Both** | Raw crawled for discovery; cleaned registered by ETL contract |

### Crawler Configuration Essentials

- **Recrawl policy:** `CRAWL_NEW_FOLDERS_ONLY` for incremental lakes
- **Schema change policy:** `UPDATE_IN_DATABASE` vs `LOG` vs `DELETE_IN_DATABASE`
- **Table grouping:** Optional — groups compatible schemas into one table
- **Schedule:** Cron for nightly catalog refresh

### Schema Evolution and Crawlers

When source CSV adds a column:

- Crawler may **add columns** to the catalog table
- Existing Parquet files won't magically gain the column — **ETL must handle backfill**
- Set `SchemaChangePolicy` intentionally; don't let crawlers delete production columns

---

## 4. Glue ETL Jobs

### Job Types

| Type | Engine | Use Case |
|------|--------|----------|
| **Spark** | PySpark / Scala | Batch transforms (this module) |
| **Python shell** | CPython 3.9 | Lightweight scripts, no distributed Spark |
| **Ray** | Ray on Glue | ML preprocessing (advanced) |

We focus on **Spark ETL jobs** with **Glue 4.0** (Spark 3.3, Python 3.10).

### Job Anatomy

```text
Script (S3) + IAM Role + Glue Version + Worker Type/Count
        │
        ▼
   Spark Driver + Executors (DPUs)
        │
        ├── Read (S3, Catalog, JDBC)
        ├── Transform (DataFrame / DynamicFrame)
        └── Write (S3 Parquet, Catalog sink)
```

### Key Parameters (Passed at Runtime)

```python
# Resolved in script via getResolvedOptions
JOB_NAME
raw_bucket
cleaned_bucket
dataset_path      # e.g. retail/orders
processing_date     # e.g. 2024-01-15
```

Pass parameters via Terraform `default_arguments`, Step Functions (Module 6), or the console.

### DynamicFrame vs DataFrame

| API | Notes |
|-----|-------|
| **DynamicFrame** | Glue-native; handles semi-structured data; `ApplyMapping`, `ResolveChoice` |
| **DataFrame** | Standard Spark SQL; preferred when schema is known |

**Course pattern:** Read with DynamicFrame or Spark CSV → convert to DataFrame → transform → write Parquet.

---

## 5. PySpark on Glue — Essentials

### Boilerplate (Glue 4.x)

```python
import sys
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glue_context = GlueContext(sc)
spark = glue_context.spark_session
job = Job(glue_context)
job.init(args["JOB_NAME"], args)
# ... transforms ...
job.commit()
```

### Common Transformations (Retail Orders)

```python
from pyspark.sql import functions as F

df = (
    df.dropDuplicates(["order_id"])
      .filter(F.col("order_id").isNotNull())
      .withColumn("total_amount", F.col("quantity") * F.col("unit_price"))
      .withColumn("processed_at", F.current_timestamp())
      .withColumn("year", F.lit("2024"))
      .withColumn("month", F.lit("01"))
      .withColumn("day", F.lit("15"))
)
```

### Writing Parquet with Partitions

```python
(
    df.write
    .mode("overwrite")  # or append for incremental — design explicitly
    .partitionBy("year", "month", "day")
    .parquet(f"s3://{cleaned_bucket}/cleaned/retail/orders/")
)
```

**Production note:** `overwrite` on a partition prefix requires dynamic partition overwrite mode in Spark 3+:

```python
spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
```

---

## 6. Raw → Cleaned ETL Design

### Responsibilities by Zone

| Zone | ETL Responsibility |
|------|---------------------|
| **Raw** | No transformation; preserve source fidelity |
| **Cleaned** | Types, nulls, dedup, PII handling, standard columns |
| **Curated** | Business models (star schema, aggregates) — Module 5 |

### Cleaned Layer Contract

Define a **schema contract** document per dataset:

- Required columns and types
- Primary key / dedup keys
- Validation rules (Module 4)
- Partition columns
- Output format (Parquet, Snappy compression)

### Example Path Flow

```text
IN:  s3://bucket/raw/retail/orders/year=2024/month=01/day=15/orders_2024-01-15.csv
OUT: s3://bucket/cleaned/retail/orders/year=2024/month=01/day=15/part-*.parquet
```

### Idempotency

Re-running the job for the same `processing_date` should produce **equivalent** cleaned output:

- Partition-level overwrite, or
- Merge/upsert with Iceberg/Delta (advanced; capstone option)

---

## 7. Schema Evolution

Schema evolution is inevitable: APIs add fields, vendors change exports, regulations require new attributes.

### Strategies

| Strategy | Description | Trade-off |
|----------|-------------|-----------|
| **Permissive reads** | New columns default to null in old partitions | Simple; query complexity |
| **Schema registry** | Enforce versions (Glue, Confluent, custom JSON) | Operational overhead |
| **Bronze preservation** | Always keep raw; rebuild cleaned on breaking changes | Storage cost |
| **Column mapping** | ETL maps `cust_id` → `customer_id` | Maintenance |

### Glue-Specific Tactics

1. **Crawler `UPDATE_IN_DATABASE`** for additive changes on raw tables
2. **Explicit `select` lists** in ETL for cleaned — ignore unknown columns until reviewed
3. **`from_csv` with `enforceSchema=false`** then cast with `when` defaults
4. **Quarantine** malformed rows (Module 4) instead of failing the job

### Breaking vs Non-Breaking Changes

| Change | Type | Action |
|--------|------|--------|
| New optional column | Non-breaking | Add to ETL select; backfill optional |
| Rename column | Breaking | Version dataset (`orders_v2`) or map in ETL |
| Type change (string → int) | Breaking | Cast with validation; quarantine failures |
| Removed column | Breaking | Document deprecation; keep null in curated until downstream updates |

---

## 8. ETL Optimization

### Storage Layout

| Technique | Impact |
|-----------|--------|
| **Parquet + Snappy** | 5–10× smaller than CSV; column pruning in Athena |
| **Partitioning** | Reduces data scanned (`year`, `month`, `day`) |
| **File sizing** | Target 128–256 MB per file; coalesce before write |
| **Avoid small files** | Too many tiny files hurts Athena and crawler performance |

### Spark / Glue Job Tuning

| Setting | Guidance |
|---------|----------|
| **Worker type** | `G.1X` (4 vCPU, 16 GB) for most labs; `G.2X` for heavy shuffles |
| **Number of workers** | Start with 2–5; scale with data volume |
| **Bookmarking** | Job bookmarks for incremental processing (S3 sources) |
| **Pushdown predicates** | Filter early; prune partitions in read path |

### Cost Controls

- Run jobs on **schedule**, not continuously
- Use **job metrics** (CloudWatch) to right-size workers
- **Compress** intermediate data; don't write debug CSVs to S3 in prod
- Tag resources for cost allocation (`Project`, `Environment`, `Student`)

### Anti-Patterns

- Reading entire raw bucket without partition filter
- `collect()` on large datasets (driver OOM)
- Excessive `repartition()` causing shuffle storms
- Writing unpartitioned Parquet for time-series fact tables

---

## 9. Observability and Operations

### CloudWatch Metrics

Glue publishes: `glue.driver.aggregate.numCompletedTasks`, runtime, bytes read/written.

### Logging

- Driver logs in CloudWatch Logs: `/aws-glue/jobs/output`
- Use structured log lines: `logger.info(f"Read {count} rows from {path}")`

### Failure Handling

| Failure | Response |
|---------|----------|
| Schema mismatch | Route bad records to quarantine; alert SNS |
| S3 permission | Fix IAM role policy (common lab issue) |
| DPU timeout | Increase workers or optimize shuffle |
| Duplicate run | Design idempotent writes per partition |

---

## 10. Security and Governance

- Glue jobs assume an **IAM role** with least privilege (S3 prefixes, Catalog, CloudWatch)
- **Never** embed credentials in scripts; use IAM roles and Secrets Manager for JDBC
- **Lake Formation** (Module 7) adds table/column ACLs on catalog resources
- Encrypt data at rest (S3 SSE) and in transit (TLS)

---

## 11. Industry Patterns

### Healthcare (HIPAA)

- Separate accounts or prefixes for PHI
- Mask identifiers in cleaned; restrict curated to minimum necessary
- Audit every job run (CloudTrail + job bookmarks metadata)

### Financial Services

- Immutable raw with WORM retention
- Reconciliation jobs compare raw record counts vs cleaned

### Retail (Our Labs)

- High-volume orders: partition by date; Snappy Parquet in cleaned
- Crawler on raw for ad-hoc exploration; contract schema in cleaned

---

## 12. Key Terminology

| Term | Definition |
|------|------------|
| **DPU** | Data Processing Unit — 4 vCPU + 16 GB (G.1X) |
| **Classifier** | Rules for inferring CSV/JSON/XML structure in crawlers |
| **Job bookmark** | Tracks processed files for incremental ETL |
| **Dynamic partition overwrite** | Overwrites only partitions present in written DataFrame |
| **Data contract** | Agreed schema and SLAs for a dataset between producer and consumer |

---

## 13. Discussion Questions

1. Why might you disable a crawler on the cleaned zone and manage schema only via ETL?
2. When is `overwrite` dangerous for a cleaned table, and how do you mitigate it?
3. How does partition pruning in Athena relate to how Glue writes Parquet?
4. What is the operational difference between schema evolution in raw vs cleaned?

---

## 14. This Week's Labs and Assignment

| Activity | Goal |
|----------|------|
| **Lab 3.1** | Deploy Glue ETL: Raw CSV → Cleaned Parquet |
| **Lab 3.2** | Configure crawlers and query via Athena |
| **Lab 3.3** | Optimize partitioning and file sizes |
| **Assignment 3** | Design healthcare ETL with PHI handling |

---

## Further Reading

- [AWS Glue Developer Guide](https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html)
- [AWS Glue Best Practices](https://docs.aws.amazon.com/glue/latest/dg/best-practices.html)
- [Optimizing Spark on Glue](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-performance.html)
- [Working with Crawlers](https://docs.aws.amazon.com/glue/latest/dg/add-crawler.html)

---

**Next:** [Lab 3.1 – Raw → Cleaned ETL](../labs/lab-3.1-etl-raw-to-cleaned/README.md)
