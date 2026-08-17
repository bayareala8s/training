# Governance – Banking Regulatory Data Platform

**Author:** Capstone Reference Implementation  
**Last Updated:** 2024-01-15  
**Scenario:** Capstone Option 1 – Banking  
**Project key:** `cnde-cap-banking`

---

## 1. Governance Overview

### Scope

Security, access control, encryption, audit logging, and compliance evidence for settlement and transaction data used in daily regulatory reporting.

### Compliance Context

| Framework / Policy | Applicable | Notes |
|--------------------|------------|-------|
| SOX (ITGC / reporting integrity) | Yes | Immutable raw, lineage manifests, change control on rules |
| PCI-DSS | Partial | No full PAN storage; card channel metadata only |
| GDPR / CCPA | Partial | Customer names in accounts; minimize in curated exports |
| AWS Shared Responsibility Model | Yes | AWS secures infrastructure; we secure data & IAM |

### Data Classification

| Classification | Examples | Handling |
|----------------|----------|----------|
| **Internal** | Aggregated settlement totals | Encrypted; analyst read on curated |
| **Confidential** | Account balances, customer names | Restricted IAM; no public buckets |
| **Restricted** | Raw transaction extracts | ETL roles only; long retention |

---

## 2. Identity and Access Management

### Principles

1. Least privilege per zone (raw write ≠ curated read)
2. Separation of duties: ingestion ≠ compliance admin
3. Prefer IAM roles; no long-lived keys in Glue
4. Tag-based scoping: `Project=capstone-option-1`

### IAM Roles

| Role | Purpose | Key Permissions |
|------|---------|-----------------|
| `capstone-ingestion-role` | Landing files to raw | `s3:PutObject` on `raw/*` |
| `capstone-glue-etl-role` | Quality + curated ETL | Read raw; write cleaned/curated/quarantine/metadata |
| `capstone-athena-compliance-role` | Settlement reporting | `s3:GetObject` on `curated/*`; Athena |
| `capstone-steward-role` | Quarantine triage | Read quarantine + quality reports |

### Human Access

| Persona | Zones Allowed | MFA |
|---------|---------------|-----|
| Data engineer | All (dev) | Required |
| Compliance analyst | curated + metadata | Required |
| Risk steward | quarantine + cleaned | Required |
| Auditor (read-only) | curated + metadata manifests | Required |

---

## 3. Encryption & Network

| Control | Implementation |
|---------|----------------|
| At rest | S3 SSE-S3 default; KMS CMK for production accounts |
| In transit | TLS for S3/Athena/Glue |
| Bucket policy | Deny non-HTTPS; block public access ON |
| Secrets | No credentials in sample data or Glue scripts |

---

## 4. Audit Trails & Lineage

| Artifact | Location | Purpose |
|----------|----------|---------|
| Quality report per dataset | `metadata/quality-reports/` | Pass/fail counts |
| Pipeline run manifest | `metadata/pipeline-runs/` | Processing date, project, reports |
| Quarantine payloads | `quarantine/{dataset}/` | Rule-level evidence |
| CloudTrail | AWS account | API-level who/when |

Raw zone objects are treated as **append-only / overwrite-by-partition** only via pipeline roles—manual deletes require dual control in production.

---

## 5. Data Quality as a Control

Validation rules under `src/validation/rules/` enforce:

- Identifier formats (transaction, settlement, account IDs)
- Amount ranges preventing negative or absurd values
- Allowed currencies and lifecycle statuses
- Required settlement dates for reportability

Failed records never enter curated settlement summaries, protecting regulatory totals.

---

## 6. Retention & Disposal

| Zone | Retention | Disposal |
|------|-----------|----------|
| raw | 7 years | Lifecycle → Glacier → expire |
| cleaned | 24 months | Expire |
| curated | 36 months | Expire after archive export |
| quarantine | 90 days | Expire after steward SLA |

---

## 7. Incident Response (Data Quality)

1. Alert when pass rate &lt; 90% for settlements
2. Steward reviews `quarantine/settlements`
3. Fix source feed or adjust rules via PR review
4. Re-run partition; update run manifest
5. Document in change log for SOX evidence

---

## 8. Tagging Standard

```text
Project=capstone-option-1
Course=cloud-native-data-engineering
Environment=dev
Owner=cnde-cap-banking
DataClassification=Confidential
```
