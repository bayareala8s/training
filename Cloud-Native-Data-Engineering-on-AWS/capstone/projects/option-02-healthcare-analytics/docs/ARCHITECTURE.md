# Architecture – Healthcare Analytics Platform

**Author:** Capstone Reference Implementation  
**Last Updated:** 2024-01-15  
**Scenario:** Capstone Option 2 – Healthcare  
**Project key:** `cnde-cap-healthcare`

> All datasets are synthetic. Design patterns are HIPAA-aware; this is not a certified BAA environment.

---

## 1. Executive Summary

### Problem Statement

Operations leaders need department-level appointment metrics and lab trend facts, but raw EHR extracts contain SSNs and emails that must not appear in analyst marts. Invalid IDs and out-of-range clinical values also pollute dashboards when quality is enforced only downstream.

### Solution Overview

A medallion lake stores immutable synthetic raw extracts, validates with Lab 4.1 rule types, quarantines failures, and curates:

1. **Patients** – SSN masked to `***-**-XXXX`, email replaced with SHA-256 hash  
2. **Appointments** – aggregated **appointments_by_department** summary  
3. **Lab results** – typed clinical facts with abnormal/critical flags  

Local execution uses `../../_shared/run_pipeline.py`. AWS reuse path uploads to the course lab bucket; optional Glue job mirrors transforms in PySpark.

### Success Criteria

| Criterion | Target |
|-----------|--------|
| Daily pipeline completion | By 07:00 UTC |
| Patient curated without raw SSN/email | 100% of passed rows |
| Appointment summary freshness | ≤ 6 hours |
| Monthly AWS cost (lab) | ≤ $25 |

---

## 2. Requirements

### Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | Ingest patients, appointments, lab_results | Must |
| FR-2 | Validate + quarantine | Must |
| FR-3 | Mask SSN and hash email in curated patients | Must |
| FR-4 | Department appointment summary | Must |
| FR-5 | Audit manifests for access/quality | Must |
| FR-6 | Athena-ready curated outputs | Should |

### Non-Functional Requirements

| Category | Requirement |
|----------|-------------|
| **Security** | Encryption; least privilege; no public buckets |
| **Compliance** | HIPAA-aware controls; minimum necessary in curated |
| **Privacy** | Synthetic data only in this course artifact |
| **Observability** | Quality pass rates + CloudWatch when deployed |
| **Cost** | Tag `Project=capstone-option-2`; lifecycle policies |

---

## 3. Data Flow

| Stage | Input | Process | Output |
|-------|-------|---------|--------|
| Ingest | CSV/JSON | Immutable copy | `raw/` |
| Quality | Raw | RuleEngine | `cleaned/` + `quarantine/` |
| Curate patients | Cleaned | Mask/hash | `curated/patients/` |
| Curate appointments | Cleaned | Group by department | `curated/appointments/` |
| Curate labs | Cleaned | Flags / types | `curated/lab_results/` |
| Audit | Metrics | Manifest | `metadata/` |

Diagrams: [architecture/diagrams/architecture.md](../architecture/diagrams/architecture.md).

---

## 4. AWS Service Selection

| Layer | Service | Justification |
|-------|---------|---------------|
| Storage | S3 | Lake zones + retention |
| ETL | Glue (optional) / local Python | Managed Spark + offline path |
| Analytics | Athena | Serverless SQL on curated |
| Catalog | Glue Data Catalog | Table definitions |
| Security | IAM + KMS + CloudTrail | Access + audit |
| Monitoring | CloudWatch + SNS | Job/quality alerts |

---

## 5. Data Zone Design

| Zone | Purpose | Retention | Consumers |
|------|---------|-----------|-----------|
| raw | Source of truth (synthetic PHI-like) | 6 years | ETL only |
| cleaned | Validated | 12 months | ETL |
| curated | Masked / aggregated | 24 months | Analysts (limited) |
| quarantine | Failed rows | 90 days | Privacy / data stewards |
| metadata | Quality + lineage | 6 years | Compliance |

### Curated patient columns (privacy)

| Column | Notes |
|--------|-------|
| ssn_masked | `***-**-` + last 4 |
| email_hash | SHA-256 of normalized email |
| first_name / last_name | Retained for ops demo; production would tokenize further |

---

## 6. ETL Design

### Job: `cnde-cap-healthcare-glue`

| Attribute | Value |
|-----------|-------|
| Trigger | Daily / manual lab |
| Worker | G.1X · 2 DPU |
| Idempotency | Partition overwrite by processing date |

---

## 7. Design Decisions

### Decision 1: Mask in curated, not only in BI

- **Rationale:** Analysts querying Athena should never see raw SSN/email even with broad SQL access to curated.  
- **Trade-off:** Raw zone still holds synthetic identifiers for reprocessing—locked to ETL roles.

### Decision 2: Department rollup for appointments

- **Rationale:** Ops KPIs are department-centric; detail remains in cleaned for clinical ops with tighter roles.  
- **Trade-off:** Patient-level appointment mart deferred.

### Decision 3: Reuse `lab-cycle.sh`

- Avoid duplicate Terraform; tag `Project=capstone-option-2`.

---

## 8. Future Enhancements

| Enhancement | Priority |
|-------------|----------|
| Lake Formation column filters / cell filters | High |
| Tokenization service for names | Medium |
| FHIR ingest adapters | Medium |
| Step Functions + SNS on critical lab spikes | Medium |

---

## 9. References

- Course Module 4 – Data Quality (Lab 4.1)  
- Capstone Option 2 requirements  
- AWS HIPAA whitepapers (design guidance only)
