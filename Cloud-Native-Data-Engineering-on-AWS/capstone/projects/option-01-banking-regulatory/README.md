# Capstone Project – Banking Regulatory Data Platform

**Student:** Capstone Reference Implementation  
**Scenario:** Option 1 – Banking Regulatory Data Platform  
**Project key:** `cnde-cap-banking`  
**Course:** Cloud-Native Data Engineering on AWS

---

## Overview

Regional banks must produce auditable daily settlement reports for regulators and internal risk teams. This project implements a cloud-native medallion data lake that ingests **transactions**, **settlements**, and **accounts**, validates every record with Lab 4.1-style declarative rules, quarantines failures, and publishes a curated **daily_settlement_summary** grouped by settlement date, currency, and status—with encryption, least-privilege access, and immutable audit lineage.

## Architecture Summary

```text
Core Banking / Clearing Files
        │
        ▼
   sample-data / S3 raw/
        │
        ▼
 RuleEngine (not_null · range · enum · regex)
        │
   ┌────┴────┐
   ▼         ▼
cleaned/  quarantine/
   │
   ▼
 curated/  →  daily_settlement_summary (+ txn & account views)
   │
   ▼
 Athena / compliance analysts   ·   CloudWatch quality reports
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) and [architecture/diagrams/architecture.md](architecture/diagrams/architecture.md).

## Prerequisites

- Python 3.10+
- Optional AWS: course lab stack via `./scripts/lab-cycle.sh start`, AWS CLI, `BUCKET` env var

## How to Run (Local Pipeline)

```bash
cd capstone/projects/option-01-banking-regulatory

# Regenerate synthetic sample data (optional)
python3 src/ingestion/generate_sample_data.py

# Run quality → cleaned → curated → reports
bash scripts/run_local.sh
```

Outputs land under `output/`:

| Path | Contents |
|------|----------|
| `output/raw/` | Partitioned copies of source files |
| `output/cleaned/` | Records that passed validation |
| `output/quarantine/` | Failed records with violation details |
| `output/curated/` | Business-ready CSV (incl. daily_settlement_summary) |
| `output/metadata/` | Quality reports + pipeline run manifest |

## Optional AWS Upload

Reuse the shared course lab environment, then upload pipeline outputs:

```bash
# From repo root – start / reuse lab infrastructure
./scripts/lab-cycle.sh start

export BUCKET=<your-lab-datalake-bucket>

cd capstone/projects/option-01-banking-regulatory
python3 ../_shared/run_pipeline.py --project-root . --upload --bucket "$BUCKET"
```

Objects are written under `s3://$BUCKET/capstone/cnde-cap-banking/`. Tag resources with `Project=capstone-option-1` (see [infrastructure/README.md](infrastructure/README.md)).

## Datasets

| Dataset | Format | Approx. rows | Notes |
|---------|--------|--------------|-------|
| transactions | CSV | ~50 | 5 intentional bad rows for quarantine demo |
| settlements | CSV | ~20 | Aggregated into daily_settlement_summary |
| accounts | JSON | ~15 | 2 intentional bad rows |

## Deliverables Checklist

- [x] README with local + optional AWS instructions
- [x] Architecture documentation and Mermaid diagrams
- [x] Governance / SOX-oriented controls documentation
- [x] Cost analysis for a realistic lab footprint
- [x] Presentation outline + demo script
- [x] Sample data with quarantine-worthy bad records
- [x] Validation rules (≥5 per primary dataset)
- [x] Curated transforms including `daily_settlement_summary`
- [x] Glue-ready ETL script
- [x] Local runner script (`scripts/run_local.sh`)
- [x] Infrastructure reuse notes (`Project=capstone-option-1`)

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Governance](docs/GOVERNANCE.md)
- [Cost Analysis](docs/COST-ANALYSIS.md)
- [Presentation Outline](presentation/outline.md)

## Tags

```text
Project=capstone-option-1
Course=cloud-native-data-engineering
Environment=dev
Owner=cnde-cap-banking
```
