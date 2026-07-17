# Reference Solution — Module 07 (Instructor Only)

**Do not distribute to students.**  
**Case study:** NorthStar Financial Services (fictional)

---

## Exemplar posture

- Data: settlement objects = Restricted; evidence = Confidential; SNS notifications = Internal
- Trust boundaries: Identity → IAM roles; Control → KMS key policy; Data → prefix-scoped S3; Detect → CloudWatch/SNS
- RTO ≤ 4 hours; RPO ≤ 15 minutes for lab slice
- CRR off; simulated DR runbook documented
- Recovery drill restores prior version; elapsed time recorded; optional Lambda metric

## Sample STRIDE priorities

1. Information disclosure via broad List/Get (High)
2. Tampering / destructive delete without restore drill (High)
3. Elevation via wildcard IAM (High)
4. Repudiation via missing evidence trails (Medium)

## Sample control-evidence rows

| Risk | Control objective | Implementation | Evidence |
| ---- | ----------------- | -------------- | -------- |
| Disclosure | Encrypt Restricted at rest with CMK | SSE-KMS default encryption | `kms_key_arn`, bucket encryption config |
| Overbroad access | Least privilege by prefix | Writer/reader role policies | Role ARNs + policy JSON |
| Accidental loss | Retain versions; tested restore | S3 versioning + drill notes | list-object-versions output; timestamps |
| Undetected failures | Detective alerting | CW alarms + SNS | Alarm names from outputs |
| Untested DR | Organizational readiness | Simulated DR runbook | Runbook section in submission |

## ADR stance (exemplar)

**Decision:** Do not enable CRR for v1 lab/reference platform; rely on versioning + quarterly restore drills; revisit CRR if business funds Tier-1 region impairment coverage.

## Grading notes

Award excellence for explicit residual risk and cleanup confirmation. Penalize public access, wildcards without justification, or missing drill evidence.
