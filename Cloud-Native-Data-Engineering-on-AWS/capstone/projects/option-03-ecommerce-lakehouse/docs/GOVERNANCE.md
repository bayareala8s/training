# Governance & Security – E-Commerce Analytics Lakehouse

**Project:** `cnde-cap-ecommerce`  
**Scenario:** Capstone Option 3

---

## 1. Data Classification

| Dataset | Classification | Notes |
|---------|----------------|-------|
| orders | Internal / Confidential | Contains customer_id + amounts |
| products | Internal | Catalog; low sensitivity |
| customers | Confidential (PII) | Email is PII |
| clickstream | Internal | Session behavior; linkable to customer_id |

---

## 2. PII Handling

- Raw zone retains source emails for replay and audit.
- Curated `dim_customers` stores **masked** emails (`ab***@example.com`).
- Athena workgroup should deny `SELECT` on raw customer files for analyst roles.
- No payment card data in this domain (PCI out of scope); if added later, tokenize upstream.

---

## 3. Access Control

| Role | Raw | Cleaned | Curated | Quarantine |
|------|-----|---------|---------|------------|
| Pipeline role | RW | RW | RW | RW |
| Analyst | — | — | R | — |
| Steward | R | R | R | RW |
| Admin | RW | RW | RW | RW |

IAM principles:

- Separate job role vs human SSO roles
- Bucket policies deny non-HTTPS
- Resource tags: `Project=capstone-option-3`

---

## 4. Encryption & Retention

- S3 default encryption (SSE-S3 or SSE-KMS)
- TLS in transit for all AWS API/S3 access
- Raw: 730 days → Glacier/IA lifecycle optional
- Quarantine: 90 days then expire after steward review

---

## 5. Quality as a Control

Quality rules are governance controls, not just engineering niceties:

- Invalid amounts/statuses never reach `fact_orders`
- Quarantine JSON includes `_violations` for audit
- Run manifests under `metadata/pipeline-runs/` provide lineage of each processing_date

---

## 6. Compliance Alignment

| Concern | Control |
|---------|---------|
| Accuracy of financial KPIs | Amount/status validation + quarantine |
| Privacy (GDPR-like) | Masking in curated dims; minimize raw analyst access |
| Change management | Versioned rules JSON (`version: 1.0`) |
| Least privilege | Role matrix above |

---

## 7. Audit Checklist

- [ ] Confirm tags on bucket/job: `Project=capstone-option-3`
- [ ] Review latest quality reports pass rates
- [ ] Spot-check quarantine for false positives
- [ ] Verify curated email masking
- [ ] Confirm Athena workgroup output location is encrypted
