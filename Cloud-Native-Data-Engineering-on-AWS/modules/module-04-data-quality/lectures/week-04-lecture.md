# Week 4 Lecture: Data Quality & Reliability Engineering

**Duration:** 2 hours · **Module 4**

---

## Learning Objectives

By the end of this lecture you will:

1. Define data quality dimensions and translate business rules into technical validation
2. Design a reusable validation framework with declarative rule definitions
3. Implement error handling strategies that fail safely without losing data
4. Architect quarantine zones for bad-record isolation and remediation
5. Apply reliability engineering patterns (SLIs, SLOs, idempotency) to data pipelines
6. Evaluate open-source quality tools such as Great Expectations and AWS-native alternatives

---

## 1. Why Data Quality Matters

Data pipelines that move data without validating it create **downstream debt**. A single bad record can:

- Inflate revenue reports by millions of dollars
- Break ML models trained on corrupted features
- Trigger incorrect inventory replenishment
- Violate regulatory reporting requirements

**Data engineering responsibility:** Quality is not a downstream analyst problem. Engineers must enforce validation **at ingestion and transformation boundaries**—before data reaches curated zones consumed by the business.

### The Cost of Bad Data

| Impact Area | Example Failure | Business Consequence |
|-------------|-----------------|----------------------|
| Finance | Negative order amounts | Incorrect revenue recognition |
| Operations | Duplicate customer IDs | Failed fulfillment, angry customers |
| Marketing | Invalid email formats | Campaign bounces, wasted spend |
| Compliance | Missing audit timestamps | Regulatory fines |

---

## 2. Data Quality Dimensions

Industry frameworks (DAMA-DMBOK, ISO 8000) define quality across multiple dimensions. In practice, data engineers focus on these six:

| Dimension | Question | Example Rule |
|-----------|----------|--------------|
| **Completeness** | Are required fields present? | `customer_id IS NOT NULL` |
| **Validity** | Does data conform to allowed values? | `status IN ('pending','shipped','cancelled')` |
| **Accuracy** | Does data reflect reality? | Order total matches sum of line items |
| **Consistency** | Is data uniform across systems? | SKU format matches catalog standard |
| **Timeliness** | Is data fresh enough? | Event timestamp within 5 minutes of ingestion |
| **Uniqueness** | Are there duplicates? | One row per `order_id` per day |

**Key insight:** You cannot validate every dimension on every dataset. Prioritize rules based on **downstream impact** and **regulatory requirements**.

---

## 3. Validation Architecture

### Where to Validate

```text
Source System
     │
     ▼
┌─────────────┐    Lightweight checks     ┌─────────────┐
│  Ingestion  │ ─── (schema, size, hash) ─→│  Raw Zone   │
└─────────────┘                            └──────┬──────┘
                                                  │
                                                  ▼
                                           ┌─────────────┐
                                           │  ETL / Glue │ ← Full validation rules
                                           └──────┬──────┘
                                                  │
                              ┌───────────────────┼───────────────────┐
                              ▼                   ▼                   ▼
                        Cleaned Zone         Quarantine          Quality Report
                        (pass records)    (fail records)       (metrics + alerts)
```

### Validation Layers

| Layer | When | What to Check | Tools |
|-------|------|---------------|-------|
| **Structural** | Ingestion | File format, schema, row count | Lambda, Glue classifier |
| **Field-level** | Bronze → Silver | not_null, range, enum, regex | Custom validators, GE |
| **Record-level** | Silver transform | Cross-field logic, referential integrity | Spark, SQL |
| **Dataset-level** | Post-batch | Volume anomalies, distribution drift | Deequ, custom metrics |
| **Pipeline-level** | Continuous | Freshness, job success rate | CloudWatch, Step Functions |

---

## 4. Quality Rules: From Business to Code

### Declarative Rule Definitions

Enterprise teams define rules in **JSON or YAML** so analysts and engineers share a single source of truth:

```json
{
  "dataset": "retail/orders",
  "version": "1.0",
  "rules": [
    {
      "name": "order_id_not_null",
      "field": "order_id",
      "type": "not_null",
      "severity": "error",
      "message": "Every order must have an identifier"
    },
    {
      "name": "amount_positive",
      "field": "order_amount",
      "type": "range",
      "params": { "min": 0.01, "max": 50000 },
      "severity": "error"
    },
    {
      "name": "status_valid",
      "field": "status",
      "type": "enum",
      "params": { "values": ["pending", "shipped", "delivered", "cancelled"] },
      "severity": "error"
    },
    {
      "name": "email_format",
      "field": "customer_email",
      "type": "regex",
      "params": { "pattern": "^[\\w.+-]+@[\\w.-]+\\.[a-zA-Z]{2,}$" },
      "severity": "warning"
    }
  ]
}
```

### Rule Types Reference

| Type | Purpose | Params |
|------|---------|--------|
| `not_null` | Reject missing values | — |
| `range` | Numeric bounds | `min`, `max` |
| `enum` | Allowed categorical values | `values` (list) |
| `regex` | Pattern matching | `pattern` |
| `unique` | No duplicates within batch | `fields` (optional composite key) |
| `freshness` | Data recency | `max_age_hours` |

### Severity Levels

| Severity | Behavior | Use When |
|----------|----------|----------|
| **error** | Record quarantined; pipeline may fail | Business-critical violations |
| **warning** | Record passes with flag in metadata | Soft quality issues for monitoring |
| **info** | Logged only | Trend tracking, non-blocking checks |

---

## 5. Error Handling Strategies

Bad data will arrive. How you handle it defines platform trust.

### Anti-Patterns (Never Do This)

1. **Silent drop** — Remove bad records without logging or quarantine
2. **Fail entire batch** — One bad row blocks 1M good rows from processing
3. **Default values everywhere** — `NULL → 0` corrupts analytics silently
4. **Validate only in production** — Rules must run in dev/staging too

### Recommended Pattern: Route and Report

```text
For each record:
  1. Run all applicable rules
  2. Collect violations with rule name, field, actual value
  3. If any ERROR severity → route to quarantine with violation metadata
  4. If WARNING only → pass to cleaned with quality_flags column
  5. Emit batch metrics: pass_count, fail_count, rule_breakdown
```

### Idempotency and Reprocessing

When a pipeline re-runs:

- Quarantine paths should include **batch_id** and **run_timestamp** to avoid overwrites
- Cleaned zone writes should be **partition-scoped idempotent** (delete + insert or merge)
- Reprocessing quarantined records after fix requires a **replay workflow** (Lab 4.3)

---

## 6. Quarantine Zones

The quarantine zone (introduced in Module 1) is the **safe holding area** for records that fail validation.

### S3 Path Convention

```text
s3://{bucket}/quarantine/{domain}/{dataset}/year={YYYY}/month={MM}/day={DD}/
    run_id={uuid}/
        failed_records.parquet
        violations.json
        _SUCCESS
```

### Quarantine Record Schema

Each quarantined record should carry:

| Field | Description |
|-------|-------------|
| `_original_record` | Full source payload (JSON or struct) |
| `_violations` | List of `{rule, field, message, severity}` |
| `_quarantine_timestamp` | UTC ISO-8601 |
| `_source_path` | S3 key of raw input |
| `_batch_id` | Pipeline run identifier |

### Quarantine Lifecycle

```text
Raw → Validate → FAIL → Quarantine
                      ↓
              Data Steward reviews
                      ↓
         Fix source OR approve override
                      ↓
              Replay job → Cleaned
```

**Retention:** Quarantine data often has shorter lifecycle (30–90 days) than raw. Configure S3 lifecycle rules accordingly.

---

## 7. Reliability Engineering for Data Pipelines

Data pipelines are **distributed systems**. Apply SRE concepts from Google and AWS Well-Architected Reliability pillar.

### SLIs and SLOs for Data

| SLI (Indicator) | Measurement | Example SLO |
|-----------------|-------------|---------------|
| **Freshness** | Time since last successful curated update | Orders curated within 2 hours of source event, 99.5% of days |
| **Completeness** | % records passing validation | ≥ 99.9% pass rate for orders |
| **Accuracy** | Reconciliation variance vs source | Revenue within 0.01% of ERP |
| **Availability** | Pipeline job success rate | 99.9% monthly job success |
| **Latency** | End-to-end processing time | Batch completes within 45 minutes |

### Error Budgets

If your SLO is 99.9% completeness and you process 1M orders/day:

- **Error budget:** 1,000 bad records/day before SLO breach
- Use budget for: planned schema changes, source system migrations
- When budget exhausted: freeze deployments, escalate to source team

### Designing for Failure

| Pattern | Application |
|---------|-------------|
| **Retries with backoff** | Transient S3/Glue API failures |
| **Dead-letter queues** | Lambda ingestion failures → SQS DLQ |
| **Circuit breaker** | Stop processing if fail rate > 5% in a batch |
| **Checkpointing** | Glue job bookmarks for incremental recovery |
| **Alerting** | CloudWatch alarms on quarantine volume spikes |

---

## 8. Great Expectations Concepts

[Great Expectations (GX)](https://greatexpectations.io/) is a popular open-source framework for data validation and documentation.

### Core Concepts

| GX Concept | Data Engineering Equivalent |
|------------|----------------------------|
| **Expectation** | A single validation rule (e.g., `expect_column_values_to_not_be_null`) |
| **Expectation Suite** | Collection of rules for one dataset |
| **Checkpoint** | Runnable validation job against a batch of data |
| **Data Context** | Configuration store (filesystem or S3) |
| **Validation Result** | JSON/HTML report of pass/fail |
| **Data Docs** | Auto-generated documentation site |

### Example Expectation (Python)

```python
validator.expect_column_values_to_be_between(
    column="order_amount",
    min_value=0.01,
    max_value=50000,
)
validator.expect_column_values_to_be_in_set(
    column="status",
    value_set=["pending", "shipped", "delivered", "cancelled"],
)
```

### GX vs Custom Validators vs AWS Deequ

| Approach | Pros | Cons |
|----------|------|------|
| **Great Expectations** | Rich docs, community, Spark/Pandas support | Operational overhead, learning curve |
| **Custom Python (Lab 4.1)** | Full control, lightweight, no extra deps | You maintain the framework |
| **AWS Deequ** | Native Spark on Glue, anomaly detection | Spark-only, JVM/Python interop |
| **Glue Data Quality** | Managed, integrated with Glue Studio | AWS-specific, rule DSL |

**Course approach:** Lab 4.1 builds a custom framework you fully understand. Lab 4.2 integrates it into Lambda/Glue—the same patterns apply when adopting GX or Deequ later.

---

## 9. Quality Reporting for Stakeholders

Technical validation must produce **business-readable output**.

### Daily Quality Report Structure

```json
{
  "report_date": "2024-01-15",
  "dataset": "retail/orders",
  "batch_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "summary": {
    "total_records": 10000,
    "passed": 9847,
    "quarantined": 153,
    "pass_rate_pct": 98.47
  },
  "top_violations": [
    { "rule": "amount_positive", "count": 89 },
    { "rule": "status_valid", "count": 42 },
    { "rule": "email_format", "count": 22 }
  ],
  "slo_status": {
    "completeness_target_pct": 99.9,
    "completeness_actual_pct": 98.47,
    "within_slo": false
  }
}
```

### Alerting Thresholds

| Condition | Action |
|-----------|--------|
| Pass rate drops > 2% day-over-day | SNS email to data team |
| Quarantine volume > 500 records/hour | PagerDuty / Slack alert |
| SLO breach for 2 consecutive days | Escalate to engineering manager |
| New rule type fails > 50% of records | Likely rule misconfiguration—halt pipeline |

Store reports in `s3://{bucket}/metadata/quality-reports/` and query with Athena for trending.

---

## 10. AWS Implementation Patterns

### Lambda: Lightweight Ingestion Validation

- Validate JSON payload schema before writing to raw
- Reject oversize files or wrong content-type
- Write validation summary to CloudWatch Logs metric filter

### Glue: Batch Validation at Scale

- Read raw Parquet/CSV with DynamicFrame
- Apply validation UDF or join against rule config
- Split DataFrame: `valid_df` → cleaned, `invalid_df` → quarantine
- Write both outputs in same job (atomic batch semantics)

### CloudWatch Metrics

Custom metrics from validation runner:

```text
Namespace: CNDE/DataQuality
Metrics:
  - RecordsProcessed (Count)
  - RecordsQuarantined (Count)
  - PassRate (Percent)
  - RuleViolations (Count) [dimensions: RuleName, Dataset]
```

---

## 11. Industry Use Cases

### Retail (RetailCo — This Module's Context)

- Order amounts must be positive; status must match fulfillment system
- Duplicate order IDs from retry logic quarantined before revenue reporting
- Daily completeness SLO: 99.9% for finance close

### Banking

- Regulatory fields (account number checksum) validated before curated layer
- Quarantine records retained 7 years for audit
- Zero tolerance for PII in wrong encryption zone

### Healthcare

- HIPAA: validation logs must not contain raw PHI in error messages
- Referential integrity between patient and encounter tables
- Freshness SLO for clinical dashboards

---

## 12. Key Terminology

| Term | Definition |
|------|------------|
| **Data contract** | Agreement between producer and consumer on schema and quality |
| **Quarantine** | Isolated storage for records failing validation |
| **Validation suite** | Named collection of rules for a dataset |
| **Pass rate** | Percentage of records meeting all error-severity rules |
| **SLI** | Service Level Indicator—a measurable quality metric |
| **SLO** | Service Level Objective—target value for an SLI |
| **Data drift** | Statistical change in data distribution over time |
| **Replay** | Reprocessing corrected or approved quarantined records |

---

## 13. Discussion Questions

1. Should a record with one ERROR and two WARNINGs go to quarantine or cleaned with flags?
2. Who owns quarantined data—the data engineering team or the source system team?
3. How do you validate referential integrity when the reference table updates hourly?
4. When would you choose Great Expectations over a custom validator library?
5. What is the right pass-rate SLO for a dataset used only for exploratory analytics?

---

## 14. This Week's Labs

| Lab | Goal |
|-----|------|
| **Lab 4.1** | Build a Python validation framework with declarative JSON rules |
| **Lab 4.2** | Integrate validation into Lambda and Glue ETL pipelines |
| **Lab 4.3** | Implement quarantine zone isolation and replay workflow |

**Assignment 4:** Define data quality SLAs for RetailCo's order and inventory datasets.

---

## Further Reading

- [AWS Glue Data Quality](https://docs.aws.amazon.com/glue/latest/dg/glue-data-quality.html)
- [Great Expectations Documentation](https://docs.greatexpectations.io/)
- [Amazon Deequ (GitHub)](https://github.com/awslabs/deequ)
- [Google SRE Book — Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)
- [DAMA-DMBOK Data Quality Dimensions](https://www.dama.org/)

---

**Next:** [Lab 4.1 – Data Quality Framework](../labs/lab-4.1-quality-framework/README.md)
