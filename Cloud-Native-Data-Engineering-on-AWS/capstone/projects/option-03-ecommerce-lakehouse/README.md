# E-Commerce Analytics Lakehouse

**Project key:** `cnde-cap-ecommerce`  
**Scenario:** Capstone Option 3  
**Course:** Cloud-Native Data Engineering on AWS

---

## Overview

ShopSphere needs a cost-efficient analytics lakehouse that turns orders, products, customers, and clickstream into a trusted star schema. This project ingests batch and event-style sample data, validates every record with Lab 4.1-style rules (`not_null`, `range`, `enum`, `regex`), quarantines failures, and curates `fact_orders` plus dimension and event summaries for Athena-friendly analytics.

## Architecture Summary

```text
OMS / PIM / CRM / Web
        │
        ▼
   Ingestion (CSV + JSON)
        │
        ▼
 S3 medallion: raw → quality → cleaned / quarantine
        │
        ▼
 Curated star schema: fact_orders + dim_products + dim_customers + events
        │
        ▼
     Athena / BI
```

Details: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) · diagrams: [architecture/diagrams/architecture.md](architecture/diagrams/architecture.md)

## Prerequisites

- Python 3.10+
- Optional AWS: CLI + course `scripts/lab-cycle.sh`

## How to Run (local pipeline)

```bash
# Regenerate synthetic samples (optional)
python3 src/ingestion/generate_sample_data.py

# Quality → cleaned → curated → reports
bash scripts/run_local.sh

# Custom processing date
bash scripts/run_local.sh --processing-date 2024-01-15
```

The script invokes `python3 ../../_shared/run_pipeline.py --project-root ..` and writes under `output/`.

### Optional AWS upload

```bash
./scripts/lab-cycle.sh start   # from course repo root
source ./scripts/lab-env.sh
cd capstone/projects/option-03-ecommerce-lakehouse
bash scripts/run_local.sh --upload --bucket "$BUCKET"
# → s3://$BUCKET/capstone/cnde-cap-ecommerce/
```

Infrastructure notes: [infrastructure/README.md](infrastructure/README.md) (tags `Project=capstone-option-3`).

## Sample Data

| Dataset | File | Approx rows | Notes |
|---------|------|-------------|-------|
| orders | `sample-data/orders.csv` | ~40 | Includes bad amounts/statuses/ids |
| products | `sample-data/products.csv` | ~15+ | Includes invalid category/price |
| customers | `sample-data/customers.csv` | ~20 | Includes bad email/segment |
| clickstream | `sample-data/clickstream.json` | ~30 | Includes bad event types/devices |

## Curated Outputs

| Dataset | Transform | Curated shape |
|---------|-----------|---------------|
| orders | `orders_curated.py` | fact_orders grain |
| products | `products_curated.py` | dim_products |
| customers | `customers_curated.py` | dim_customers (masked email) |
| clickstream | `clickstream_curated.py` | event facts + funnel_weight |

## Deliverables Checklist

- [x] README with local + optional AWS path
- [x] `pipeline.json` for shared runner
- [x] Architecture, governance, cost docs
- [x] Mermaid architecture diagrams
- [x] Presentation outline + demo script
- [x] Sample data with quarantine cases
- [x] Validation rules (≥5 per primary dataset)
- [x] Curated ETL modules (`to_curated`)
- [x] `generate_sample_data.py`
- [x] `scripts/run_local.sh`
- [x] Glue-ready `src/etl/glue_job.py`
- [x] Infrastructure README (lab-cycle + tagging)

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Governance](docs/GOVERNANCE.md)
- [Cost analysis](docs/COST-ANALYSIS.md)
- [Presentation outline](presentation/outline.md)

## Project Structure

```text
option-03-ecommerce-lakehouse/
├── README.md
├── pipeline.json
├── docs/
├── architecture/diagrams/
├── presentation/
├── sample-data/
├── scripts/run_local.sh
├── infrastructure/README.md
├── src/ingestion/generate_sample_data.py
├── src/validation/rules/
├── src/etl/*_curated.py
└── src/etl/glue_job.py
```

## Tags

```text
Project=capstone-option-3
Course=cloud-native-data-engineering
Environment=dev
```
