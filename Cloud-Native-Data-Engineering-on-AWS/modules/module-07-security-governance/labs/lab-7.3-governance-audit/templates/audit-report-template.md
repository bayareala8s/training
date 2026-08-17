# Data Platform Security Audit Report

**Organization:** _________________________  
**Report date:** _________________________  
**Auditor:** _________________________  
**Environment:** dev / staging / prod  
**Scope:** S3 data lake · IAM · KMS · CloudTrail · Athena/Glue catalog

---

## 1. Executive Summary

| Metric | Result |
|--------|--------|
| Overall posture | Pass / Pass with findings / Fail |
| Critical findings | |
| High findings | |
| Medium findings | |
| Next audit date | |

**Summary narrative (3–5 sentences):**

---

## 2. Control Assessment

| Control ID | Control Description | Status | Evidence |
|------------|---------------------|--------|----------|
| SEC-01 | S3 Block Public Access enabled | ☐ Pass ☐ Fail | |
| SEC-02 | Default encryption SSE-KMS | ☐ Pass ☐ Fail | |
| SEC-03 | Deny insecure transport (bucket policy) | ☐ Pass ☐ Fail | |
| SEC-04 | KMS key rotation enabled | ☐ Pass ☐ Fail | |
| IAM-01 | No users with `s3:*` on production bucket | ☐ Pass ☐ Fail | |
| IAM-02 | Analyst role cannot read `raw/` | ☐ Pass ☐ Fail | |
| IAM-03 | Pipeline roles scoped to bucket ARN | ☐ Pass ☐ Fail | |
| IAM-04 | Access review completed within 90 days | ☐ Pass ☐ Fail | |
| AUD-01 | CloudTrail enabled all regions | ☐ Pass ☐ Fail | |
| AUD-02 | S3 data events on PHI/raw prefixes | ☐ Pass ☐ Fail | |
| AUD-03 | Athena workgroup query logging enabled | ☐ Pass ☐ Fail | |
| GOV-01 | Data classification document published | ☐ Pass ☐ Fail | |
| GOV-02 | PII/PHI not in SNS or validation logs | ☐ Pass ☐ Fail | |
| GOV-03 | Quarantine retention policy configured | ☐ Pass ☐ Fail | |

---

## 3. IAM Role Inventory

| Role Name | Purpose | Last Access Review | Findings |
|-----------|---------|-------------------|----------|
| | | | |
| | | | |

---

## 4. S3 Bucket Configuration

**Bucket name:** _________________________

```bash
# Evidence commands (paste output excerpts)
aws s3api get-public-access-block --bucket BUCKET
aws s3api get-bucket-encryption --bucket BUCKET
aws s3api get-bucket-policy --bucket BUCKET --query Policy --output text | python -m json.tool
```

| Setting | Expected | Actual |
|---------|----------|--------|
| BlockPublicAcls | true | |
| IgnorePublicAcls | true | |
| BlockPublicPolicy | true | |
| RestrictPublicBuckets | true | |
| Default encryption | aws:kms | |

---

## 5. KMS Key Review

**Key ARN / alias:** _________________________

| Check | Pass/Fail | Notes |
|-------|-----------|-------|
| Key policy least privilege | | |
| Glue role can decrypt | | |
| Athena role can decrypt | | |
| No wildcard `kms:*` for non-admin | | |

---

## 6. CloudTrail and Logging

| Trail name | Multi-region | Log validation | S3 data events |
|------------|--------------|----------------|----------------|
| | | | |

**Sample management event (redact account IDs):**

```json
{
  "eventName": "",
  "userIdentity": { "type": "", "arn": "" },
  "eventTime": ""
}
```

---

## 7. Data Zone Access Validation

Tests performed (Lab 7.2):

| Test | Role | Expected | Actual |
|------|------|----------|--------|
| List raw/ | analyst-curated | Deny | |
| Get curated/ | analyst-curated | Allow | |
| Write quarantine/ | steward | Allow | |
| Delete curated/ | engineer (no tag) | Deny | |

---

## 8. Findings and Remediation

| ID | Severity | Finding | Recommendation | Owner | Due date |
|----|----------|---------|----------------|-------|----------|
| F-001 | Critical | | | | |
| F-002 | High | | | | |
| F-003 | Medium | | | | |

---

## 9. Sign-Off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Data Platform Lead | | | |
| Security Officer | | | |
| Compliance | | | |

---

*Template version 1.0 — Module 7 Lab 7.3 — Cloud-Native Data Engineering on AWS*
