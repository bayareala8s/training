# Capstone Project – Healthcare Analytics Platform

**Student:** Capstone Reference Implementation  
**Scenario:** Option 2 – Healthcare Analytics Platform  
**Project key:** `cnde-cap-healthcare`  
**Course:** Cloud-Native Data Engineering on AWS

> **Notice:** All patient names, SSNs, emails, and clinical values in this project are **synthetic**. No real PHI is used.

---

## Overview

Hospital operations and clinical analytics teams need appointment throughput and lab trends without exposing raw identifiers in downstream marts. This project implements a HIPAA-aware medallion lake that ingests synthetic **patients**, **appointments**, and **lab_results**, validates with Lab 4.1 declarative rules, quarantines bad rows, **masks SSN** (`***-**-XXXX`) and **hashes email** in curated patients, and publishes an **appointments-by-department** summary for operational reporting.

## Architecture Summary

```text
EHR / Scheduling / Lab Extracts  (SYNTHETIC samples)
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
 curated/ → patients (masked) · appointments_by_department · lab facts
   │
   ▼
 Athena analytics (limited roles)  ·  audit metadata
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) and [architecture/diagrams/architecture.md](architecture/diagrams/architecture.md).

## Prerequisites

- Python 3.10+
- Optional AWS: `./scripts/lab-cycle.sh start`, AWS CLI, `BUCKET` env var

## How to Run (Local Pipeline)

```bash
cd capstone/projects/option-02-healthcare-analytics

# Regenerate synthetic sample data (optional)
python3 src/ingestion/generate_sample_data.py

# Run quality → cleaned → curated → reports
bash scripts/run_local.sh
```

| Path | Contents |
|------|----------|
| `output/raw/` | Partitioned source copies |
| `output/cleaned/` | Passed validation |
| `output/quarantine/` | Failures with violation details |
| `output/curated/patients/` | Masked SSN + hashed email |
| `output/curated/appointments/` | Department summary |
| `output/metadata/` | Quality + run manifests |

## Optional AWS Upload

```bash
./scripts/lab-cycle.sh start   # from repo root

export BUCKET=<your-lab-datalake-bucket>

cd capstone/projects/option-02-healthcare-analytics
python3 ../_shared/run_pipeline.py --project-root . --upload --bucket "$BUCKET"
```

Prefix: `s3://$BUCKET/capstone/cnde-cap-healthcare/`. Tag with `Project=capstone-option-2` ([infrastructure/README.md](infrastructure/README.md)).

## Datasets

| Dataset | Format | Approx. rows | Notes |
|---------|--------|--------------|-------|
| patients | CSV | ~30 | ~4 bad rows; curated masks SSN / hashes email |
| appointments | CSV | ~40 | Curated → by department |
| lab_results | JSON | ~50 | ~3 bad rows |

## Deliverables Checklist

- [x] README with local + optional AWS instructions
- [x] Architecture + Mermaid diagrams
- [x] HIPAA-aware governance documentation
- [x] Cost analysis
- [x] Presentation outline + demo script
- [x] Synthetic sample data with quarantine rows
- [x] Validation rules (≥5 per dataset)
- [x] Curated transforms (PII masking + department summary)
- [x] Glue-ready ETL script
- [x] `scripts/run_local.sh`
- [x] Infrastructure reuse notes (`Project=capstone-option-2`)

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Governance](docs/GOVERNANCE.md)
- [Cost Analysis](docs/COST-ANALYSIS.md)
- [Presentation Outline](presentation/outline.md)

## Tags

```text
Project=capstone-option-2
Course=cloud-native-data-engineering
Environment=dev
Owner=cnde-cap-healthcare
DataClassification=Restricted-PHI-Synthetic
```
