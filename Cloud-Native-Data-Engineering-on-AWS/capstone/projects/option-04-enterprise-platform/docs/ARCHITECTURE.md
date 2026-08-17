# Architecture – Enterprise Data Platform

**Project:** `cnde-cap-enterprise`  
**Scenario:** Capstone Option 4  
**Last Updated:** 2024-01-15

---

## 1. Executive Summary

### Problem Statement

Northwind Enterprise runs retail orders, warehouse inventory, and vendor cost feeds in disconnected systems. Operations lacks a single daily KPI view, ML teams lack clean customer features, and there is no production-style orchestration, quality gate, or monitoring story that spans the full cloud-native curriculum (Modules 1–9).

### Solution Overview

Option 4 delivers an end-to-end enterprise data platform: multi-pattern ingestion into a medallion lake, Lab 4.1 declarative quality with quarantine, Glue curated transforms for `enterprise_kpi_daily` and `customer_order_features`, Step Functions orchestration (`daily_etl.asl.json`), CloudWatch dashboard widgets, and governance/cost controls. The local runner proves quality→curated offline; AWS lab-cycle provides optional cloud deployment.

### Success Criteria

| Criterion | Target |
|-----------|--------|
| Orchestrated daily run | 06:00 UTC via Step Functions |
| Quality gate | ≥ 85% pass rate or SNS alert |
| Curated products | KPI daily + customer features |
| Module coverage | Evidence for Modules 1–9 |
| Monthly AWS cost (dev) | ≤ $60 |

---

## 2. Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | Ingest orders (retail), inventory, vendor_feeds | Must |
| FR-2 | Medallion zones with quarantine + metadata | Must |
| FR-3 | ≥5 validation rules per primary dataset | Must |
| FR-4 | Curate enterprise_kpi_daily and customer_order_features | Must |
| FR-5 | Step Functions definition with retries/alerts | Must |
| FR-6 | CloudWatch dashboard widget catalog | Must |
| FR-7 | Map each course module to project evidence | Must |

---

## 3. Course Module → Evidence Map

| Module | Topic | Evidence in this project |
|--------|-------|--------------------------|
| 1 | Cloud data foundations / lake zones | `docs/ARCHITECTURE.md` zones; `output/raw|cleaned|curated|quarantine` |
| 2 | Ingestion patterns | Batch CSV orders/inventory; JSON vendor feeds; multi-branch ingest in ASL |
| 3 | Glue ETL | `src/etl/glue_job.py` Parquet KPI + features |
| 4 | Data quality | `src/validation/rules/*.json` + shared `validators.py` quarantine |
| 5 | Catalog / analytics | Curated schemas ready for Glue Catalog + Athena |
| 6 | Orchestration | `src/orchestration/daily_etl.asl.json` |
| 7 | Security & governance | `docs/GOVERNANCE.md`; tagging `Project=capstone-option-4` |
| 8 | Monitoring & ops | `monitoring/dashboard_widgets.json` |
| 9 | AI/ML data | `customer_order_features` curated product / Glue feature write |

---

## 4. Data Zones & Products

Same medallion layout as Option 3, plus an explicit **features** logical zone (`curated/customer_order_features`).

| Product | Grain | Source transform |
|---------|-------|------------------|
| customer_order_features | customer_id × feature_date | `orders_curated.py` / Glue |
| enterprise_kpi_daily | kpi_date | `inventory_curated.py` locally; Glue joins orders+inventory |
| vendor quality rows | feed_id | `vendor_feeds_curated.py` |

---

## 5. Orchestration

`daily_etl.asl.json` flow:

1. Parallel ingest (orders, inventory, vendor feeds)  
2. Validate quality  
3. Choice gate on pass_rate ≥ 85%  
4. Glue curated sync job  
5. SNS success / failure  

ARN placeholders are intentional for lab wiring—see `infrastructure/README.md`.

---

## 6. Design Decisions

1. **Full-platform scope** – Prefer breadth across modules over deep streaming.  
2. **Quality gate soft-fail to alert** – Stewards get notified; curated may still run for partial KPIs.  
3. **Features from orders** – Avoid separate feature store cost in v1; Parquet features are Feature Store–ready.  
4. **Reuse lab-cycle** – No duplicate Terraform; tags distinguish option-4 spend.

---

## 7. Future Enhancements

| Enhancement | Module affinity |
|-------------|-----------------|
| SageMaker Feature Store sync | 9 |
| Lake Formation LF-TBAC | 7 |
| MWAA for complex backfills | 6 |
| Anomaly detection on quarantine rates | 8 / 9 |

Diagrams: [architecture/diagrams/architecture.md](../architecture/diagrams/architecture.md)
