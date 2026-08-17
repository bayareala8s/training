# Architecture – E-Commerce Analytics Lakehouse

**Project:** `cnde-cap-ecommerce`  
**Scenario:** Capstone Option 3  
**Last Updated:** 2024-01-15

---

## 1. Executive Summary

### Problem Statement

ShopSphere’s merchandising and finance teams reconcile sales across OMS, catalog, CRM, and web analytics in spreadsheets. Negative amounts and invalid statuses occasionally reach dashboards, and ad-hoc Athena scans over raw CSVs inflate query spend. Leadership needs a cost-efficient lakehouse with a clear star schema, quarantine for bad records, and support for both nightly batch loads and clickstream events.

### Solution Overview

This project implements a cloud-native analytics lakehouse on AWS using a medallion layout (raw → cleaned → curated → quarantine). Declarative quality rules (Lab 4.1 style: `not_null`, `range`, `enum`, `regex`) gate promotion to curated. Curated transforms produce `fact_orders` plus dimension summaries (`dim_products`, `dim_customers`) and clickstream event facts for funnel analysis. Athena queries Parquet partitions; lifecycle policies and selective column projection keep interactive analytics inexpensive.

### Success Criteria

| Criterion | Target |
|-----------|--------|
| Daily batch completion | By 07:00 UTC |
| Orders quality pass rate | ≥ 85% |
| Curated freshness | ≤ 6 hours |
| Monthly AWS cost (dev) | ≤ $45 |

---

## 2. Requirements

### Functional

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | Ingest orders, products, customers (batch CSV) and clickstream (JSON events) | Must |
| FR-2 | Validate with ≥5 rules per primary dataset; quarantine errors | Must |
| FR-3 | Curate `fact_orders` grain: order_id, customer_id, product_id, amount, status, date | Must |
| FR-4 | Publish dim summaries for products and customers | Must |
| FR-5 | Support Athena KPI queries (GMV, AOV, funnel) | Must |
| FR-6 | Optional S3 upload of local pipeline output | Should |

### Non-Functional

| Category | Requirement |
|----------|-------------|
| Scalability | 10× order volume via partition growth only |
| Availability | Pipeline success ≥ 95% over rolling 30 days |
| Security | SSE-S3/KMS; least-privilege IAM; masked emails in dims |
| Cost | Partition pruning; Parquet; raw lifecycle to IA |
| Observability | Quality reports under `metadata/quality-reports/` |

---

## 3. Data Zones

| Zone | Purpose | Retention | Format |
|------|---------|-----------|--------|
| raw/ | Immutable source copies | 2 years | CSV/JSON |
| cleaned/ | Passed validation | 180 days | JSON |
| curated/ | Star schema facts/dims | 1 year | CSV local / Parquet on AWS |
| quarantine/ | Failed validation | 90 days | JSON + violations |
| metadata/ | Quality + run manifests | 1 year | JSON |

Path convention:

```text
…/raw/{dataset}/year=YYYY/month=MM/day=DD/
…/cleaned/{dataset}/year=YYYY/month=MM/day=DD/
…/curated/{dataset}/year=YYYY/month=MM/day=DD/
…/quarantine/{dataset}/year=YYYY/month=MM/day=DD/
```

---

## 4. Star Schema

**fact_orders** (grain: one order line)

- `order_id`, `customer_id`, `product_id`, `amount`, `quantity`, `status`, `channel`, `order_date`, `processing_date`, `gross_margin_proxy`

**dim_products** – category, brand, unit_price, price_tier, is_active  
**dim_customers** – email_masked, segment, region, lifetime_orders_est  
**clickstream events** – event_type, funnel_weight, device, session_id

Diagrams: [architecture/diagrams/architecture.md](../architecture/diagrams/architecture.md)

---

## 5. AWS Services

| Layer | Service | Justification |
|-------|---------|---------------|
| Storage | S3 | Cheap durable lake |
| ETL | Glue (Spark) | Managed; catalog-friendly |
| Quality | Lambda + shared RuleEngine | Same rules as local |
| Analytics | Athena | Serverless SQL; pay per TB scanned |
| BI | QuickSight (optional) | Star-schema dashboards |
| Orchestration | EventBridge schedule | Nightly batch + micro-batch clickstream |

---

## 6. ETL & Idempotency

- Local: `scripts/run_local.sh` → `_shared/run_pipeline.py`
- AWS: `src/etl/glue_job.py` builds `fact_orders` Parquet with partition overwrite for `processing_date`
- Re-runs for the same date replace curated partitions (idempotent for that day)

---

## 7. Design Decisions

1. **Star schema over wide flat tables** – Analysts join dims; facts stay narrow for Athena scan efficiency.  
2. **Batch + events** – Orders/dims nightly; clickstream allowed as JSON micro-batches into the same quality path.  
3. **Warnings vs errors** – Channel/region warnings do not quarantine; structural/business errors do.  
4. **Margin proxy in fact** – Simple 32% proxy avoids joining cost feeds in v1.

---

## 8. Future Enhancements

| Enhancement | Priority |
|-------------|----------|
| Kinesis / Firehose for true streaming clickstream | Medium |
| Lake Formation column filters on customer email | High |
| SCD2 for dim_customers | Medium |
| dbt semantic layer on Athena | Low |
