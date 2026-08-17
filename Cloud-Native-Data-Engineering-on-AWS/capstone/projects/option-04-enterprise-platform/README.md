# Enterprise Data Platform

**Project key:** `cnde-cap-enterprise`  
**Scenario:** Capstone Option 4  
**Course:** Cloud-Native Data Engineering on AWS

---

## Overview

Northwind Enterprise needs a full cloud-native data platform spanning medallion storage, multi-ingest, quality with quarantine, Glue curation, Step Functions orchestration, monitoring, governance, and ML-ready features. This option integrates evidence across Modules 1–9: retail orders, inventory snapshots, and vendor feeds flow through the shared local runner and optional AWS lab stack into `enterprise_kpi_daily` and `customer_order_features`.

## Architecture Summary

```text
Retail OMS · WMS · Vendor APIs
            │
   Multi-ingest (parallel)
            │
   Medallion lake + quality gate
            │
   Glue / local curated transforms
      ├─ enterprise_kpi_daily
      └─ customer_order_features
            │
   Athena / BI · optional ML consumers
            │
   Step Functions · CloudWatch · SNS
```

Module map: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) · diagrams: [architecture/diagrams/architecture.md](architecture/diagrams/architecture.md)

## Prerequisites

- Python 3.10+
- Optional AWS: CLI, `scripts/lab-cycle.sh`, Glue/SFN permissions

## How to Run (local pipeline)

```bash
python3 src/ingestion/generate_sample_data.py   # optional regenerate
bash scripts/run_local.sh
bash scripts/run_local.sh --processing-date 2024-01-15
```

Uses `python3 ../../_shared/run_pipeline.py --project-root ..`.

### Optional AWS upload

```bash
./scripts/lab-cycle.sh start    # course repo root
source ./scripts/lab-env.sh
cd capstone/projects/option-04-enterprise-platform
bash scripts/run_local.sh --upload --bucket "$BUCKET"
# → s3://$BUCKET/capstone/cnde-cap-enterprise/
```

See [infrastructure/README.md](infrastructure/README.md) (`Project=capstone-option-4`).

## Sample Data

| Dataset | File | Approx rows | Notes |
|---------|------|-------------|-------|
| orders | `sample-data/orders.csv` | ~40 | Bad ids/amounts/statuses included |
| inventory | `sample-data/inventory.csv` | ~25 | Bad sku/status/negative QOH |
| vendor_feeds | `sample-data/vendor_feeds.json` | ~20 | Bad feed ids/costs/statuses |

## Curated Outputs

| Dataset | Transform | Product |
|---------|-----------|---------|
| orders | `orders_curated.py` | `customer_order_features` |
| inventory | `inventory_curated.py` | `enterprise_kpi_daily` (local) |
| vendor_feeds | `vendor_feeds_curated.py` | vendor quality rows |

On AWS, `src/etl/glue_job.py` joins cleaned orders + inventory into Parquet KPI and feature tables.

## Platform Extras

| Artifact | Path |
|----------|------|
| Step Functions ASL | `src/orchestration/daily_etl.asl.json` |
| CloudWatch widgets | `monitoring/dashboard_widgets.json` |
| Glue job | `src/etl/glue_job.py` |

## Deliverables Checklist

- [x] README (local + AWS)
- [x] `pipeline.json`
- [x] Architecture (incl. module evidence map), governance, cost
- [x] Mermaid diagrams
- [x] Presentation outline + demo script
- [x] Sample data with bad records
- [x] Validation rules (≥5 per dataset)
- [x] Curated ETL + Glue job
- [x] `generate_sample_data.py` + `run_local.sh`
- [x] Orchestration ASL + monitoring widgets
- [x] Infrastructure README (lab-cycle + tagging)

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Governance](docs/GOVERNANCE.md)
- [Cost analysis](docs/COST-ANALYSIS.md)
- [Presentation outline](presentation/outline.md)

## Project Structure

```text
option-04-enterprise-platform/
├── README.md
├── pipeline.json
├── docs/
├── architecture/diagrams/
├── presentation/
├── monitoring/dashboard_widgets.json
├── sample-data/
├── scripts/run_local.sh
├── infrastructure/README.md
├── src/ingestion/
├── src/validation/rules/
├── src/etl/
└── src/orchestration/daily_etl.asl.json
```

## Tags

```text
Project=capstone-option-4
Course=cloud-native-data-engineering
Environment=dev
```
