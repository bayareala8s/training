# Governance – Healthcare Analytics Platform

**Author:** Capstone Reference Implementation  
**Last Updated:** 2024-01-15  
**Scenario:** Capstone Option 2 – Healthcare  
**Project key:** `cnde-cap-healthcare`

> Course artifact uses **synthetic** demographics and clinical values only. Production deployments require a Business Associate Agreement (BAA) with AWS and organizational HIPAA policies.

---

## 1. Governance Overview

### Scope

Privacy, security, access control, audit, and quality controls for patient-related analytics pipelines.

### Compliance Context

| Framework | Applicable | Notes |
|-----------|------------|-------|
| HIPAA Privacy / Security Rules | Design-aware | Minimum necessary; access controls; audit |
| AWS BAA | Required in prod | Not assumed for student accounts |
| AWS Shared Responsibility | Yes | Customer configures encryption, IAM, logging |

### Data Classification

| Classification | Examples | Handling |
|----------------|----------|----------|
| **Restricted (PHI-like)** | Raw SSN, email, names in raw/ | ETL roles only; encrypted |
| **Confidential** | Cleaned clinical facts | Limited clinical ops |
| **Internal analytics** | Department appointment summary; masked patients | Analyst roles on curated |

---

## 2. Identity and Access Management

### Principles

1. Minimum necessary access to PHI-like fields  
2. Separate ingestion, ETL, analyst, and steward roles  
3. MFA for human access  
4. Tag `Project=capstone-option-2`

### IAM Roles

| Role | Zones | Notes |
|------|-------|-------|
| `capstone-ingestion-role` | raw Put | Landing only |
| `capstone-glue-etl-role` | all lake zones | Masking happens here |
| `capstone-athena-analyst-role` | curated Get | No raw/cleaned |
| `capstone-privacy-steward-role` | quarantine + quality | Triage bad PHI rows |

### Analyst Guarantee

Curated patients **must not** contain plaintext `ssn` or `email` columns—only `ssn_masked` and `email_hash`.

---

## 3. Encryption & Logging

| Control | Implementation |
|---------|----------------|
| At rest | SSE-S3 / KMS CMK |
| In transit | TLS |
| Public access | Blocked |
| API audit | CloudTrail |
| Access to S3 | Server access logs or CloudTrail data events (prod) |

---

## 4. PII / PHI Handling

| Field | Raw | Curated |
|-------|-----|---------|
| SSN | Full synthetic `###-##-####` | `***-**-XXXX` |
| Email | Full synthetic | SHA-256 hash |
| Names | Present | Present (demo); tokenize in prod |
| Patient ID | Surrogate `PAT-######` | Retained as join key |

Hashing is one-way for analytics joins on identity without reversible email storage in curated.

---

## 5. Audit Trails

| Artifact | Purpose |
|----------|---------|
| `metadata/quality-reports/` | Validation pass rates |
| `metadata/pipeline-runs/` | Run identity + processing date |
| Quarantine JSON | Rule violations without promoting bad PHI |
| CloudTrail | Who accessed which APIs |

---

## 6. Retention

| Zone | Retention | Rationale |
|------|-----------|-----------|
| raw | 6 years | Medical record-adjacent analytics retention pattern |
| curated | 24 months | Ops analytics |
| quarantine | 90 days | Steward SLA then purge |

Secure disposal via S3 lifecycle expiration after legal hold checks in production.

---

## 7. Incident Response

1. Suspected plaintext PHI in curated → revoke analyst role, delete/overwrite partition  
2. Investigate pipeline transform regression  
3. Re-run with masking verified  
4. Document in privacy incident log  

---

## 8. Tagging

```text
Project=capstone-option-2
Course=cloud-native-data-engineering
Environment=dev
Owner=cnde-cap-healthcare
DataClassification=Restricted-PHI-Synthetic
```
