# Assignment 4: Data Quality SLAs for Retail

**Due:** End of Week 4 · **Weight:** Part of Assignments (20%)

---

## Scenario

**RetailCo** (from Assignment 1) now has a deployed S3 data lake with Raw, Cleaned, Curated, and Quarantine zones. Glue ETL jobs process daily orders and inventory feeds. Finance closes books at 6 AM UTC and requires validated order data in the curated zone by 5 AM UTC.

Recent incidents exposed quality gaps:

- 847 orders with negative amounts reached curated tables before manual detection
- Supplier inventory feed included SKUs with invalid warehouse codes, causing fulfillment errors
- Clickstream events had 3% duplicate `event_id` values, inflating conversion metrics
- No documented SLAs—teams disagree on acceptable pass rates and freshness windows

Your data platform lead asks you to define a **Data Quality SLA program** for two critical datasets.

---

## Your Task

Design and document data quality SLAs for **orders** and **inventory** datasets. Your submission becomes the team’s operational contract with source system owners and downstream consumers.

---

## Deliverables

Submit a document (3–4 pages) containing:

### 1. Executive Summary (½ page)

- Current quality risks and business impact
- Proposed SLA framework overview
- Expected outcomes (faster detection, finance confidence, reduced manual cleanup)

### 2. Dataset SLA Definitions (1½ pages)

For **each** dataset (orders, inventory), provide:

#### Orders (`retail/orders`)

| Element | Your Definition |
|---------|-----------------|
| **Completeness SLO** | Target pass rate for error-severity rules |
| **Freshness SLO** | Maximum latency from source to curated |
| **Accuracy SLO** | Reconciliation tolerance vs source ERP |
| **Availability SLO** | Pipeline job success rate |
| **Validation rules** | Minimum 5 rules with type and severity |
| **Quarantine policy** | Retention, review SLA, escalation path |
| **Error budget** | Allowed failures per month at stated volume |

#### Inventory (`retail/inventory`)

Same table structure. Include supplier-feed-specific rules (e.g., SKU format, warehouse codes).

### 3. Validation Rules Catalog (1 page)

Provide machine-readable rules in JSON for both datasets. Minimum **5 rules per dataset**.

**Orders example (extend with your own rules):**

```json
{
  "dataset": "retail/orders",
  "version": "1.0",
  "slos": {
    "completeness_pct": 99.9,
    "freshness_hours": 2,
    "pipeline_success_pct": 99.5
  },
  "rules": [
    {
      "name": "order_id_not_null",
      "field": "order_id",
      "type": "not_null",
      "severity": "error"
    },
    {
      "name": "amount_in_range",
      "field": "order_amount",
      "type": "range",
      "params": { "min": 0.01, "max": 50000 },
      "severity": "error"
    },
    {
      "name": "status_valid",
      "field": "status",
      "type": "enum",
      "params": {
        "values": ["pending", "shipped", "delivered", "cancelled"]
      },
      "severity": "error"
    },
    {
      "name": "email_format",
      "field": "customer_email",
      "type": "regex",
      "params": {
        "pattern": "^[\\w.+-]+@[\\w.-]+\\.[a-zA-Z]{2,}$"
      },
      "severity": "warning"
    },
    {
      "name": "currency_valid",
      "field": "currency",
      "type": "enum",
      "params": { "values": ["USD", "EUR", "GBP", "CAD"] },
      "severity": "error"
    }
  ]
}
```

**Inventory example (starter):**

```json
{
  "dataset": "retail/inventory",
  "version": "1.0",
  "slos": {
    "completeness_pct": 99.5,
    "freshness_hours": 26,
    "pipeline_success_pct": 99.0
  },
  "rules": [
    {
      "name": "sku_not_null",
      "field": "sku",
      "type": "not_null",
      "severity": "error"
    },
    {
      "name": "quantity_non_negative",
      "field": "quantity_on_hand",
      "type": "range",
      "params": { "min": 0, "max": 1000000 },
      "severity": "error"
    },
    {
      "name": "warehouse_valid",
      "field": "warehouse_code",
      "type": "enum",
      "params": {
        "values": ["WH-EAST", "WH-WEST", "WH-CENTRAL"]
      },
      "severity": "error"
    },
    {
      "name": "sku_format",
      "field": "sku",
      "type": "regex",
      "params": { "pattern": "^SKU-[A-Z0-9]{6,12}$" },
      "severity": "error"
    },
    {
      "name": "last_updated_not_null",
      "field": "last_updated",
      "type": "not_null",
      "severity": "warning"
    }
  ]
}
```

### 4. Monitoring and Alerting Plan (½ page)

Define:

- CloudWatch metrics to publish (namespace, metric names, dimensions)
- Alarm thresholds tied to SLOs
- SNS routing (who gets paged vs emailed)
- Daily quality report format and audience

Reference Lab 4.2 patterns.

### 5. Incident Response Playbook (½ page)

When an SLO is breached:

1. **Detect** — How is the breach identified?
2. **Triage** — Who owns initial response?
3. **Contain** — Stop bad data reaching curated (circuit breaker?)
4. **Remediate** — Quarantine review and replay steps
5. **Post-mortem** — What to document within 48 hours

Include a **decision matrix**:

| Pass Rate | Freshness | Action |
|-----------|-----------|--------|
| ≥ SLO | On time | Normal operations |
| 99.0–99.9% | On time | Warning alert; steward review within 24h |
| < 99.0% | On time | Halt curated publish; escalate to engineering |
| Any | > 2× SLO window | Page on-call; finance notified if orders affected |

---

## Grading Rubric

| Criterion | Points |
|-----------|--------|
| SLA definitions realistic and measurable | 25 |
| Validation rules catalog (completeness, correctness) | 25 |
| Monitoring/alerting aligned to SLOs | 20 |
| Incident response playbook | 15 |
| Clarity, professionalism, JSON validity | 15 |
| **Total** | **100** |

---

## Submission Format

- File: `assignment-04-{your-name}.md` or PDF
- Include both JSON rule files inline or as attachments
- Optional: run Lab 4.1 against a custom sample and attach `quality_report.json`

---

## Reference Paths

```text
s3://retailco-prod-datalake/raw/retail/orders/year=2024/month=01/day=15/
s3://retailco-prod-datalake/cleaned/retail/orders/year=2024/month=01/day=15/
s3://retailco-prod-datalake/quarantine/retail/orders/year=2024/month=01/day=15/run_id={uuid}/
s3://retailco-prod-datalake/metadata/quality-reports/retail/orders/2024-01-15_report.json
s3://retailco-prod-datalake/raw/suppliers/inventory/year=2024/month=01/day=15/
```

---

## Tips

- Reference [Week 4 Lecture](../lectures/week-04-lecture.md) SLI/SLO concepts
- Orders need stricter completeness (finance); inventory may tolerate lower freshness (daily supplier feed)
- Distinguish **error** (quarantine) vs **warning** (pass with flag) severities
- Tie error budgets to monthly order volume (~500K/day from Assignment 1)
- Consider Great Expectations as a future migration path—design rules that translate cleanly

---

**Next week:** [Module 5 – Data Modeling & Analytics](../../module-05-modeling-analytics/README.md)
