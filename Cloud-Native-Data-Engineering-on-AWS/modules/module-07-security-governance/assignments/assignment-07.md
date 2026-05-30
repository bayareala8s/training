# Assignment 7: HIPAA Governance Framework for Healthcare Data

**Due:** End of Week 7 · **Weight:** Part of Assignments (20%)

---

## Scenario

**HealthLake Analytics** is a healthcare subsidiary building on the same AWS patterns as RetailCo. They ingest:

- **HL7/FHIR clinical encounters** → `raw/clinical/encounters/` (contains PHI)
- **Claims summaries** → `raw/finance/claims/` (contains limited PHI + financial data)
- **De-identified research cohort** → `curated/research/cohort/` (HIPAA Safe Harbor applied)

Regulatory requirements:

- HIPAA Security Rule technical safeguards
- Annual risk assessment and access reviews
- Business Associate Agreements with AWS and any SaaS integrators
- Breach notification within 60 days if PHI is exposed

Current gaps:

- Single shared IAM role can read all S3 prefixes including raw PHI
- S3 buckets use SSE-S3 only; compliance requires CMK with key rotation
- No documented governance model or audit report template
- Step Functions SNS alerts included patient names in test messages (Module 6 gap)

---

## Your Task

Produce a **HIPAA-aligned data governance framework** for the HealthLake data platform. This document will be reviewed by security and compliance officers before production launch.

---

## Deliverables

Submit a document (5–6 pages) containing:

### 1. Executive Summary (½ page)

- Regulatory scope and business context
- Top three risks in current state
- Framework overview and implementation phases

### 2. Data Classification and Zone Model (1 page)

| Zone | Classification | PHI Allowed | Encryption | Example Tables |
|------|----------------|-------------|------------|----------------|
| raw/clinical/ | | | | |
| cleaned/clinical/ | | | | |
| curated/analytics/ | | | | |
| quarantine/clinical/ | | | | |

Include Mermaid diagram of zones and allowed data flows (no PHI to unrestricted curated).

### 3. IAM and Access Control Matrix (1½ pages)

Define roles:

| Role | raw/clinical | cleaned/clinical | curated/analytics | Athena | Glue jobs |
|------|--------------|------------------|-------------------|--------|-----------|
| platform-engineer | | | | | |
| clinical-analyst | | | | | |
| research-analyst | | | | | |
| audit-readonly | | | | | |
| pipeline-glue-role | | | | | |

Use **least privilege** (Allow + explicit Deny for PHI where needed). Reference Lab 7.2 patterns.

### 4. Encryption and Key Management (1 page)

- CMK strategy (single vs per-zone keys)
- Key rotation and alias naming
- Bucket default encryption configuration
- `aws:SecureTransport` and deny unencrypted upload policies
- Break-glass key usage procedure

### 5. PII/PHI Handling Procedures (1 page)

- Field-level classification examples (MRN, diagnosis, ZIP code)
- Masking vs tokenization vs redaction decisions
- Validation/quarantine rules (Module 4) — no PHI in logs or SNS
- Minimum necessary standard for analyst views

### 6. Audit and Monitoring Plan (1 page)

| Control | Tool | Retention | Review Cadence |
|---------|------|-----------|----------------|
| API management events | CloudTrail | | |
| S3 object access | | | |
| Athena queries | | | |
| IAM policy changes | | | |

Include sample entries from Lab 7.3 audit report template.

### 7. Incident Response and Breach Notification (½ page)

- Detection triggers
- Containment steps (disable role, block bucket policy)
- Assessment timeline aligned to 60-day notification rule
- Post-incident documentation

### 8. Governance Operating Model (½ page)

- RACI for policies, access reviews, and steward assignments
- Quarterly access review process
- Lake Formation adoption roadmap (Phase 1 IAM → Phase 2 LF)

---

## Grading Rubric

| Criterion | Points |
|-----------|--------|
| Zone model and PHI isolation | 25 |
| IAM matrix least-privilege and Deny usage | 25 |
| Encryption and KMS design | 20 |
| Audit plan and template usage | 15 |
| Incident response and operating model | 10 |
| Clarity, regulatory alignment, professionalism | 5 |
| **Total** | **100** |

---

## Submission Format

- File: `assignment-07-{your-name}.md` or PDF
- Attach completed [Lab 7.3 audit report template](../labs/lab-7.3-governance-audit/templates/audit-report-template.md) as appendix (filled with sample data)

---

## Tips

- Reference [Week 7 Lecture](../lectures/week-07-lecture.md) HIPAA mapping table
- Research cohort must not re-identify (Safe Harbor 18 identifiers)
- Pipeline roles need write to raw/cleaned but analysts do not
- Cross-reference Module 6 SNS sanitization requirements

---

**Next week:** [Module 8 – Monitoring, Cost Optimization & Operations](../../module-08-monitoring-ops/README.md)
