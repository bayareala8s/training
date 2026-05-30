# Governance – [Project Name]

**Author:** [Your Name]  
**Last Updated:** [Date]  
**Scenario:** Capstone Option [1–4]

---

## 1. Governance Overview

### Scope

This document defines security, access control, compliance, and audit requirements for the [Project Name] data platform.

### Compliance Context

| Framework / Policy | Applicable | Notes |
|--------------------|------------|-------|
| [HIPAA / SOX / PCI-DSS / GDPR / Internal] | Yes / Partial / No | [Explain] |
| AWS Shared Responsibility Model | Yes | AWS secures cloud; we secure data and access |

### Data Classification

| Classification | Examples | Handling |
|----------------|----------|----------|
| **Public** | Aggregated sales reports | Standard encryption |
| **Internal** | Operational metrics | IAM-restricted, encrypted |
| **Confidential** | Customer PII, account data | Masked in curated; restricted IAM |
| **Restricted** | [PHI / PCI / SSN] | Encrypted, audit logged, minimal access |

---

## 2. Identity and Access Management

### Principles

1. **Least privilege** — Grant minimum permissions required
2. **Separation of duties** — Ingestion role ≠ admin role
3. **No long-lived credentials** — Prefer IAM roles over access keys
4. **Tag-based access** — Where supported, scope by `Project=capstone`

### IAM Roles

| Role | Purpose | Key Permissions |
|------|---------|-----------------|
| `capstone-ingestion-role` | Lambda S3 writes to raw/ | `s3:PutObject` on `raw/*` |
| `capstone-glue-etl-role` | Glue job execution | S3 read/write on lake; Glue catalog |
| `capstone-athena-analyst-role` | Read curated for queries | `s3:GetObject` on `curated/*`; Athena |
| `capstone-admin-role` | Terraform deployment | Broad (dev only; not for daily use) |

### IAM Policy Example (Glue ETL – Template)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
      "Resource": [
        "arn:aws:s3:::BUCKET_NAME/raw/*",
        "arn:aws:s3:::BUCKET_NAME/cleaned/*",
        "arn:aws:s3:::BUCKET_NAME/curated/*",
        "arn:aws:s3:::BUCKET_NAME/quarantine/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": ["glue:*"],
      "Resource": ["arn:aws:glue:REGION:ACCOUNT:*"]
    }
  ]
}
```

Replace `BUCKET_NAME`, `REGION`, `ACCOUNT` with your values.

### Human Access

| Persona | Access Method | Zones Allowed |
|---------|---------------|---------------|
| Data Engineer | IAM user / SSO | raw, cleaned, curated, quarantine |
| Data Analyst | Athena workgroup | curated only |
| Data Steward | Console + Athena | quarantine, metadata |
| Auditor | Read-only CloudTrail | Audit logs only |

---

## 3. Encryption

### At Rest

| Resource | Method | Key |
|----------|--------|-----|
| S3 data lake | SSE-S3 or SSE-KMS | [aws/s3 or CMK ARN] |
| Glue job bookmarks | SSE-S3 | Default |
| CloudWatch Logs | SSE | AWS managed |

### In Transit

- All AWS API calls over TLS 1.2+
- S3 bucket policy denies non-HTTPS (`aws:SecureTransport`)

### Key Management

[Describe KMS key policy if using CMK; rotation schedule]

---

## 4. PII and Sensitive Data Handling

### PII Inventory

| Field | Dataset | Zone Present | Masking Strategy |
|-------|---------|--------------|------------------|
| `customer_email` | orders | raw, cleaned | Hashed in curated |
| `customer_name` | orders | raw | Dropped in curated |
| [Add fields] | | | |

### Masking Rules

```text
raw/       → Full fidelity (restricted access)
cleaned/   → Validated; PII still present for stewardship
curated/   → Masked/tokenized for analytics
```

### Example Transformation

[Describe how email is hashed or replaced with token]

---

## 5. Audit and Logging

### CloudTrail

- **Management events:** Enabled for all regions (or home region)
- **Data events (optional):** S3 object-level logging on sensitive prefixes

### Application Logs

| Log Group | Retention | Contents |
|-----------|-----------|----------|
| `/aws/lambda/capstone-ingestion` | 30 days | Ingestion events |
| `/aws-glue/jobs/output` | 14 days | ETL stdout |
| `/aws-glue/jobs/error` | 30 days | ETL errors |

### Audit Questions We Can Answer

1. Who accessed `curated/` data last week?
2. When was IAM policy X last modified?
3. Which Glue job run wrote to quarantine on [date]?

---

## 6. Data Quality Governance

### Stewardship Model

| Dataset | Data Owner | Steward | Quality SLA |
|---------|------------|---------|-------------|
| [orders] | [Team] | [Name] | [Pass rate, freshness] |
| [inventory] | [Team] | [Name] | [SLA] |

### Quarantine Process

1. Failed records routed to `quarantine/` with `run_id`
2. Steward notified via SNS (warning topic)
3. Review within [24/48] hours
4. Remediate source or approve replay
5. Document resolution in metadata

### Lineage

[Describe how you track data from source to curated—Glue catalog, manual doc, OpenLineage future]

---

## 7. Scenario-Specific Controls

### [Banking – Option 1]

- Immutable raw retention for [N] years
- Segregation of duties for settlement data
- Daily reconciliation report to metadata/

### [Healthcare – Option 2]

- PHI never in curated without de-identification
- BAA considerations for AWS services used
- Access reviews quarterly

### [E-Commerce – Option 3]

- Clickstream IP anonymization
- GDPR delete request handling (conceptual)

### [Enterprise – Option 4]

- Central data catalog ownership
- Cross-team access request workflow

[Delete sections that don't apply; expand the one that matches your scenario]

---

## 8. Risk Register

| Risk | Likelihood | Impact | Mitigation | Owner |
|------|------------|--------|------------|-------|
| Unauthorized S3 access | Low | High | Block public access, IAM least privilege | [You] |
| PII exposure in Athena | Medium | High | Masking in curated, workgroup restrictions | [You] |
| Undetected pipeline failure | Medium | Medium | CloudWatch alarms, SNS | [You] |
| Cost overrun | Medium | Low | Budget alerts, lifecycle policies | [You] |

---

## 9. Review Schedule

| Activity | Frequency | Owner |
|----------|-----------|-------|
| IAM access review | Monthly (dev) / Quarterly (prod) | Data platform lead |
| Encryption config audit | Quarterly | Security |
| Quality SLA review | Monthly | Data stewards |
| Disaster recovery test | Annually | Engineering |

---

## 10. References

- Module 7 – Security & Governance lecture
- [AWS S3 Security Best Practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)
- Assignment 8 – Operations runbook (incident cross-reference)
