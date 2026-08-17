# Lab 3.3 Architecture — ETL Optimization (Partitioning and Parquet)

Optimize RetailCo Glue ETL performance and Athena query costs through file coalescing, partition pruning, worker tuning, and Spark adaptive execution.

## Before vs After Optimization

```mermaid
flowchart TB
    subgraph before["Before Optimization"]
        B_RAW["Raw CSV<br/>multiple daily partitions"]
        B_JOB["Glue Job<br/>G.1X × 2 workers<br/>no coalesce"]
        B_OUT["Many tiny Parquet files<br/>per partition"]
        B_ATH["Athena full table scan<br/>high data scanned"]
    end

    subgraph after["After Optimization"]
        A_RAW["Raw CSV<br/>2024-01-15 through 2024-01-19"]
        A_JOB["Glue Job<br/>G.1X × 3 workers<br/>coalesce + AQE enabled"]
        A_OUT["1–N files ~128–256 MB<br/>per partition"]
        A_ATH["Athena partition filter<br/>minimal data scanned"]
    end

    subgraph metrics["Measured Improvements"]
        DPU["Lower DPU-seconds"]
        FILES["Fewer files per partition"]
        SCAN["Reduced Athena scan cost"]
    end

    B_RAW --> B_JOB --> B_OUT --> B_ATH
    A_RAW --> A_JOB --> A_OUT --> A_ATH
    B_ATH -.->|"optimize"| A_ATH
    A_JOB --> DPU
    A_OUT --> FILES
    A_ATH --> SCAN
```

## Optimization Pipeline

```mermaid
flowchart LR
    subgraph ingest["Multi-Day Raw Data"]
        R1["raw/retail/orders/<br/>day=15, 17, 18, 19"]
    end

    subgraph etl["Optimized Glue ETL"]
        SCRIPT["glue_etl_job_optimized.py"]
        SPARK["Spark with AQE<br/>adaptive.coalescePartitions"]
        COAL["df.coalesce(target_files)"]
    end

    subgraph storage["Optimized Cleaned Output"]
        P1["cleaned/retail/orders/<br/>year=2024/month=01/day=17/<br/>coalesced Parquet"]
    end

    subgraph query["Cost-Efficient Analytics"]
        ATH["Amazon Athena"]
        QF["Query B: WHERE year/month/day"]
        QC["Query C: SELECT specific columns"]
    end

    R1 --> SCRIPT
    SCRIPT --> SPARK --> COAL --> P1
    P1 --> ATH
    ATH --> QF
    ATH --> QC
```

## Athena Query Cost Comparison

```mermaid
flowchart TD
    subgraph queries["Athena Query Patterns"]
        QA["Query A: COUNT(*) — no filter<br/>Scans ALL partitions"]
        QB["Query B: WHERE year/month/day<br/>Partition pruning"]
        QC["Query C: SELECT 2 columns + filter<br/>Column + partition pruning"]
    end

    subgraph cost["Data Scanned"]
        HIGH["High cost"]
        MED["Medium cost"]
        LOW["Low cost"]
    end

    QA --> HIGH
    QB --> LOW
    QC --> LOW
```

## Key Components

| Component | AWS Service | Purpose |
|-----------|-------------|---------|
| Optimized ETL Script | AWS Glue + S3 | Coalesced Parquet writes at `glue/scripts/glue_etl_job.py` |
| Glue Workers | AWS Glue | Right-sized `G.1X` worker count (2–5) for cost/performance balance |
| Spark AQE | AWS Glue (Spark) | Adaptive query execution for runtime partition coalescing |
| Cleaned Parquet | Amazon S3 | Snappy-compressed, right-sized files in Hive partitions |
| Glue Data Catalog | AWS Glue | Partition metadata enabling Athena partition pruning |
| Athena | Amazon Athena | SQL analytics with scan cost measurement |
| CloudWatch | Amazon CloudWatch | Job metrics: ExecutionTime, DPUSeconds |

## S3 Path Conventions

| Path | Pattern | Optimization Notes |
|------|---------|-------------------|
| Raw (multi-day) | `s3://{bucket}/raw/retail/orders/year={Y}/month={M}/day={D}/orders_{date}.csv` | Load 2024-01-15, 17, 18, 19 for meaningful benchmarks |
| Cleaned (optimized) | `s3://{bucket}/cleaned/retail/orders/year={Y}/month={M}/day={D}/part-*.parquet` | Target 1–N files per partition via `coalesce()` |
| ETL script | `s3://{bucket}/glue/scripts/glue_etl_job.py` | Overwrite with optimized variant |

### Optimization Techniques Applied

| Technique | Where Applied | Expected Impact |
|-----------|---------------|-----------------|
| File coalescing | Glue ETL write step | Fewer, larger Parquet files per partition |
| Dynamic partition overwrite | Spark config | Idempotent re-runs without full dataset rewrite |
| Partition pruning | Athena WHERE clause | Scan only target day partition |
| Column pruning | Athena SELECT clause | Read only required Parquet columns |
| Worker tuning | Terraform `number_of_workers` | Balance DPU-seconds vs runtime SLA |
| AQE | Spark `--conf` settings | Adaptive shuffle partition coalescing |

### Baseline vs Optimized Metrics

| Metric | Before | After (Target) |
|--------|--------|----------------|
| DPU-seconds | Higher | 20–50% reduction |
| Files per partition | Many small files | 1–N coalesced files |
| Athena Query A scan | Full table | N/A (avoid in production) |
| Athena Query B scan | N/A | Single partition only |
