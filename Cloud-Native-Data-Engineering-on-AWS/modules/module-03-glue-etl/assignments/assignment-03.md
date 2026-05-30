# Assignment 3: Healthcare ETL Design with AWS Glue

**Due:** End of Week 3 · **Weight:** Part of Assignments (20%)

---

## Scenario

**HealthBridge Analytics** is a healthcare technology company that aggregates clinical and operational data for hospital networks. They are migrating from on-premises Informatica jobs to a cloud-native lake on AWS.

**Data sources:**

- **HL7/FHIR JSON exports** — patient encounters, diagnoses (daily API pull)
- **Claims CSV files** — billing records from payer SFTP (nightly)
- **EHR PostgreSQL** — provider master data (CDC via DMS, Module 2 reference)
- **IoT CSV streams** — remote patient monitoring vitals (hourly batches)

**Volume:** ~50M encounter records/year, ~2M claims/month, vitals arriving every hour for 10K monitored patients.

**Regulatory context:**

- HIPAA applies to all datasets containing PHI (Protected Health Information)
- Minimum necessary access principle for analysts
- 6-year audit retention for claims; encounter raw data retained 7 years
- Business associate agreements (BAAs) in place with AWS

**Current pain points:**

- Schema changes from EHR vendor break monthly ETL jobs
- Analysts query CSV directly — slow and expensive
- No centralized catalog; teams duplicate S3 path logic
- PII appears in curated dashboards intended for operational metrics only

---

## Your Task

Design a **production AWS Glue ETL architecture** that transforms data from Raw → Cleaned → Curated (high-level curated design only) for HealthBridge. Focus on ETL engineering, catalog strategy, schema evolution, and HIPAA-aware patterns.

---

## Deliverables

Submit a document (3–4 pages) plus diagrams containing:

### 1. Executive Summary (½ page)

- Problem statement
- Proposed Glue-centric ETL approach
- Expected outcomes (compliance, performance, analyst self-service)

### 2. ETL Pipeline Diagram

Include:

- S3 zones (raw, cleaned, curated, quarantine)
- Glue jobs per dataset (encounters, claims, providers, vitals)
- Glue Crawlers vs job-managed catalog tables
- Athena as consumption layer
- CloudWatch monitoring and SNS alerts on failure

Use Draw.io, Lucidchart, Mermaid, or legible hand-drawn scan.

### 3. Dataset ETL Specifications (1½ pages)

For **each** of the four datasets, specify:

| Field | Encounters | Claims | Providers | Vitals |
|-------|------------|--------|-----------|--------|
| Raw format & path | | | | |
| Cleaned format & path | | | | |
| Partition keys | | | | |
| Primary dedup key | | | | |
| PHI columns | | | | |
| Masking/tokenization in cleaned | | | | |
| Glue job type (Spark vs Python shell) | | | | |
| Incremental strategy | | | | |

### 4. Schema Evolution Strategy (½ page)

Address:

- How you detect schema changes (crawler policies, contract tests)
- Additive vs breaking change workflow
- Backfill approach when EHR adds required fields
- Versioning strategy (`encounters_v1` vs single table)

### 5. Optimization and Cost (½ page)

Include:

- Parquet and compression choices
- Partition design for Athena (justify vitals hourly vs daily partitions)
- Glue worker sizing approach
- 3 concrete cost controls (tags, schedules, lifecycle, etc.)

### 6. Security and Compliance (½ page)

Address:

- IAM least privilege for Glue roles (prefix-scoped S3)
- Encryption (at rest and in transit)
- How PHI is prevented from curated operational dashboards
- Audit logging (CloudTrail, job run history)

---

## Example S3 Paths (Reference)

```text
s3://healthbridge-prod-datalake/raw/fhir/encounters/year=2024/month=01/day=15/
s3://healthbridge-prod-datalake/cleaned/clinical/encounters/year=2024/month=01/day=15/
s3://healthbridge-prod-datalake/curated/clinical/daily_census/year=2024/month=01/
s3://healthbridge-prod-datalake/quarantine/clinical/encounters/year=2024/month=01/day=15/
```

---

## Grading Rubric

| Criterion | Points |
|-----------|--------|
| ETL pipeline completeness | 25 |
| Dataset specifications (all 4) | 25 |
| Schema evolution strategy | 15 |
| Optimization and cost | 15 |
| Security / HIPAA considerations | 10 |
| Clarity and professionalism | 10 |
| **Total** | **100** |

---

## Submission Format

- File: `assignment-03-{your-name}.md` or PDF
- Embed or attach architecture diagram
- Submit via your learning platform

---

## Tips

- Reference patterns from Labs 3.1–3.3 (Raw → Cleaned Parquet, crawlers, partitioning)
- Vitals data is high-frequency — explain trade-offs between hourly partitions and compaction
- Not all datasets need the same crawler policy; justify per dataset
- Quarantine zone usage earns credit (Module 4 preview)
- Avoid storing credentials in Glue scripts; use IAM roles and Secrets Manager for JDBC

---

## Optional Stretch Goal (+10 bonus points)

Propose how **Glue Job Bookmarks** or **Iceberg/Delta Lake** would improve incremental loads for encounters. One paragraph with pros/cons is sufficient.

---

**Reference:** [Week 3 Lecture](../lectures/week-03-lecture.md) · [Lab 3.1](../labs/lab-3.1-etl-raw-to-cleaned/README.md)
