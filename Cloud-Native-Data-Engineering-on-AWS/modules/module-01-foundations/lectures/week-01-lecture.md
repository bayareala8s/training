# Week 1 Lecture: Modern Data Engineering Foundations

**Duration:** 2 hours · **Module 1**

---

## Learning Objectives

By the end of this lecture you will:

1. Define data engineering and distinguish it from data science and analytics
2. Compare data lakes, data warehouses, and lakehouse architectures
3. Explain batch vs streaming processing and when to use each
4. Design a medallion (Raw → Cleaned → Curated) data lake architecture
5. Map AWS services to each layer of a cloud-native data platform

---

## 1. What Is Data Engineering?

Data engineering is the discipline of designing, building, and operating systems that **collect, transform, store, and deliver** data reliably at scale.

### Data Engineering vs Data Science vs Analytics

| Role | Primary Question | Key Output |
|------|------------------|------------|
| **Data Engineer** | How do we move and transform data reliably? | Pipelines, platforms, datasets |
| **Data Scientist** | What patterns exist in the data? | Models, experiments |
| **Data Analyst** | What happened and why? | Reports, dashboards |
| **Analytics Engineer** | How do we model data for self-serve analytics? | dbt models, semantic layers |

Data engineers build the **platform** that scientists and analysts depend on. Without reliable pipelines, downstream teams cannot trust their data.

### The Modern Data Stack (Simplified)

```text
Sources → Ingestion → Storage → Transform → Serve → Consume
                                              ↓
                                         Governance
                                         Monitoring
                                         Security
```

---

## 2. Data Lakes vs Data Warehouses

### Data Warehouse

- **Schema-on-write:** Structure defined before loading
- Optimized for SQL analytics and BI
- Examples: Amazon Redshift, Snowflake, BigQuery
- Best for: Structured reporting, known query patterns

### Data Lake

- **Schema-on-read:** Raw data stored in native format
- Supports structured, semi-structured, and unstructured data
- Examples: Amazon S3 + Athena, ADLS, GCS
- Best for: Diverse sources, exploration, ML workloads

### Lakehouse

Combines lake flexibility with warehouse performance and governance:

- Open table formats (Iceberg, Delta Lake, Hudi)
- ACID transactions on object storage
- Unified batch and streaming

**In this course:** We build a **lake-first architecture** on S3 with Glue and Athena—the pattern used by thousands of AWS enterprise customers.

---

## 3. Batch vs Streaming

| Dimension | Batch | Streaming |
|-----------|-------|-----------|
| Latency | Minutes to hours | Seconds to minutes |
| Complexity | Lower | Higher |
| Cost | Generally lower | Generally higher |
| Use cases | Reporting, ETL, ML training | Fraud detection, IoT, real-time dashboards |
| AWS services | Glue, Step Functions, Batch | Kinesis, MSK, Lambda |

**Enterprise reality:** Most platforms use **both**. Batch for historical loads and streaming for time-sensitive events. Module 2 covers event-driven patterns; Module 6 covers orchestration.

### Lambda Architecture (Conceptual)

```text
         Batch Layer (historical) ──→ Serving Layer ←── Speed Layer (real-time)
                                              ↓
                                         Query / Analytics
```

---

## 4. Data Platform Architecture

### Medallion Architecture (Bronze / Silver / Gold)

We implement this as **Raw → Cleaned → Curated** on S3:

| Zone | Also Called | Contents | Consumers |
|------|-------------|----------|-----------|
| **Raw** | Bronze | Unmodified source data | ETL jobs only |
| **Cleaned** | Silver | Validated, typed, deduplicated | ETL, quality teams |
| **Curated** | Gold | Business-ready, modeled | Analysts, Athena, ML |

Additional zones:

- **Quarantine:** Failed validation records (Module 4)
- **Metadata:** Schema definitions, lineage, data dictionaries

### Reference Architecture on AWS

```text
┌─────────────────────────────────────────────────────────────┐
│                      DATA SOURCES                            │
│   APIs · Files · Databases · SaaS · IoT · Events            │
└──────────────────────────┬──────────────────────────────────┘
                           │
              ┌────────────▼────────────┐
              │   INGESTION LAYER       │
              │ Lambda · EventBridge    │
              │ AppFlow · DMS (optional)│
              └────────────┬────────────┘
                           │
              ┌────────────▼────────────┐
              │   S3 DATA LAKE          │
              │ raw/ cleaned/ curated/│
              └────────────┬────────────┘
                           │
              ┌────────────▼────────────┐
              │   PROCESSING LAYER      │
              │ AWS Glue · Lambda       │
              └────────────┬────────────┘
                           │
              ┌────────────▼────────────┐
              │   METADATA & CATALOG    │
              │ AWS Glue Data Catalog   │
              └────────────┬────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
    Amazon Athena    Redshift/Spectrum   SageMaker
         │                 │                 │
         └─────────────────┴─────────────────┘
                           │
              ┌────────────▼────────────┐
              │   OBSERVABILITY         │
              │ CloudWatch · SNS        │
              └─────────────────────────┘
```

---

## 5. AWS Data Ecosystem

### Storage & Catalog

| Service | Purpose |
|---------|---------|
| **Amazon S3** | Durable object storage for the data lake |
| **AWS Glue Data Catalog** | Central metadata repository (Hive-compatible) |
| **AWS Lake Formation** | Fine-grained access control on the lake |

### Ingestion & Integration

| Service | Purpose |
|---------|---------|
| **AWS Lambda** | Serverless event-driven ingestion |
| **Amazon EventBridge** | Event bus for decoupled workflows |
| **AWS AppFlow** | SaaS connector (Salesforce, SAP, etc.) |
| **AWS DMS** | Database replication |

### Processing

| Service | Purpose |
|---------|---------|
| **AWS Glue** | Managed Spark ETL, crawlers, catalog |
| **Amazon EMR** | Large-scale Spark/Hadoop clusters |
| **AWS Step Functions** | Workflow orchestration |

### Analytics

| Service | Purpose |
|---------|---------|
| **Amazon Athena** | Serverless SQL on S3 |
| **Amazon Redshift** | Data warehouse |
| **Amazon QuickSight** | BI and dashboards |

### Governance & Security

| Service | Purpose |
|---------|---------|
| **IAM** | Identity and access management |
| **AWS KMS** | Encryption key management |
| **AWS CloudTrail** | API audit logging |

---

## 6. Enterprise Design Principles

1. **Immutable raw layer** — Never overwrite source data; append only
2. **Partition for performance** — Use `year/month/day` or business keys
3. **Prefer columnar formats** — Parquet over CSV for analytics
4. **Metadata-driven pipelines** — Catalog-first, not hard-coded paths
5. **Fail safely** — Quarantine bad data; never silently drop records
6. **Infrastructure as Code** — Terraform for reproducibility
7. **Cost awareness** — Lifecycle policies, query optimization, tagging

---

## 7. Industry Use Cases

### Banking
Regulatory reporting requires auditable pipelines with lineage from source to report. Raw zone retention supports compliance audits.

### Healthcare
HIPAA requires encryption, access controls, and audit trails. PII stays in cleaned zone with masking before curated analytics.

### Retail
High-volume clickstream and order data ingested via events; curated star schemas power sales and inventory dashboards.

### Government
Open data platforms publish curated datasets while raw internal data remains restricted via IAM and Lake Formation.

---

## 8. Key Terminology

| Term | Definition |
|------|------------|
| **ETL** | Extract, Transform, Load |
| **ELT** | Extract, Load, Transform (transform in warehouse/engine) |
| **Data lineage** | Tracking data from source to destination |
| **Schema evolution** | Handling changing source schemas over time |
| **Idempotency** | Re-running a pipeline produces the same result |
| **Partition** | Logical subdivision of data for efficient queries |
| **Crawler** | Automated schema discovery tool (Glue) |

---

## 9. Discussion Questions

1. Why store raw data if we always transform it before analytics?
2. When would you choose Redshift over Athena?
3. How does the medallion architecture support data governance?
4. What happens if two pipelines write to the same S3 prefix?

---

## 10. This Week's Labs

| Lab | Goal |
|-----|------|
| **Lab 1.1** | Deploy S3 data lake with Terraform |
| **Lab 1.2** | Implement zone structure and upload sample data |

**Assignment 1:** Design a data platform architecture for a retail e-commerce company (2–3 pages + diagram).

---

## Further Reading

- [AWS Building Data Lakes](https://docs.aws.amazon.com/whitepapers/latest/building-data-lakes/)
- [Amazon S3 Best Practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/best-practices.html)
- [The Data Engineering Cookbook](https://github.com/andkret/Cookbook) (community resource)

---

**Next:** [Lab 1.1 – Build S3 Data Lake](../labs/lab-1.1-build-s3-data-lake/README.md)
