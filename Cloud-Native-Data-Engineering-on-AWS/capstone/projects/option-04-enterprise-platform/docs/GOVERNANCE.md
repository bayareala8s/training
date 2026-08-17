# Governance & Security – Enterprise Data Platform

**Project:** `cnde-cap-enterprise`  
**Scenario:** Capstone Option 4

---

## 1. Data Classification

| Dataset | Classification | Handling |
|---------|----------------|----------|
| orders | Confidential | Customer + commercial amounts |
| inventory | Internal | Operational stock positions |
| vendor_feeds | Confidential | Supplier unit costs (competitive) |

Vendor unit costs are restricted to procurement and platform roles—not general analysts.

---

## 2. Security Controls

| Control | Implementation |
|---------|----------------|
| Encryption at rest | S3 SSE-S3/SSE-KMS on lake bucket |
| Encryption in transit | TLS only; deny insecure transport |
| Identity | IAM roles for Glue, Step Functions, Lambda |
| Network | Private Glue connections optional in prod |
| Tagging | `Project=capstone-option-4` on all resources |
| Secrets | No embedded credentials; use IAM + SSM if extending APIs |

---

## 3. Access Matrix

| Principal | Raw | Cleaned | Curated KPI | Features | Vendor curated | Quarantine |
|-----------|-----|---------|-------------|----------|----------------|------------|
| ETL / SFN role | RW | RW | RW | RW | RW | RW |
| BI analyst | — | — | R | — | — | — |
| ML engineer | — | — | R | R | — | — |
| Procurement | — | — | R | — | R | — |
| Steward | R | R | R | R | R | RW |

---

## 4. Quality & Change Control

- Rules JSON versioned (`version: 1.0`); bumps require steward approval
- Step Functions quality gate at 85% pass rate triggers SNS
- Quarantine payloads retain `_violations` for audit evidence
- Pipeline run manifests record processing_date lineage

---

## 5. Compliance Themes

| Theme | Approach |
|-------|----------|
| SOX-like financial integrity | Amount/status validation before KPI publication |
| Vendor confidentiality | Separate curated path; IAM deny for BI on vendor costs |
| Operational resilience | Alarms on Glue/SFN failures; documented runbook in presentation |
| Data minimization | Features store aggregates, not raw PII beyond customer_id |

---

## 6. Monitoring as Governance

Dashboard widgets (`monitoring/dashboard_widgets.json`) expose:

- Pipeline success/failure (accountability)
- Quality pass rate vs SLO (control effectiveness)
- Quarantine volume (steward workload)

---

## 7. Audit Checklist

- [ ] Tags present: `Project=capstone-option-4`
- [ ] ASL ARNs replaced before production schedule
- [ ] SNS topic subscribers verified
- [ ] Latest quality reports reviewed
- [ ] Feature and KPI partitions match processing_date
- [ ] Lab stack stopped when idle
