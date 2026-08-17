# Cost Estimate — Lab 07 Security & Resilience

**Module:** 07  
**Case study:** NorthStar Financial Services (fictional)  
**Last updated:** 2026-07-15  
**Region assumption:** `us-east-1` primary; optional `us-west-2` replica

> **Cost warning:** These are instructional estimates, not quotes. Actual spend varies by account, free-tier eligibility, object volume, alarm actions, and whether cross-region replication is enabled. Always set a budget alert and run cleanup the same day.

---

## Design choices that keep cost low

| Choice | Effect |
| ------ | ------ |
| No NAT Gateway | Avoids ~$32+/month fixed charge |
| No always-on EC2 / EKS / OpenSearch | Avoids continuous compute |
| DynamoDB on-demand | Pennies for lab item counts |
| Lambda only for drill helper | Seconds of runtime |
| CRR **off by default** | Avoids ongoing replication + dual storage |

---

## Baseline scenario (recommended classroom default)

Assumptions: deploy ~2 hours, <50 objects, CRR disabled, one email SNS subscription, cleanup same day.

| Service | Estimate |
| ------- | -------- |
| S3 storage + requests | < $0.10 |
| KMS key + API requests | < $0.50 (key ≈ $1/month prorated if left; destroy schedules deletion) |
| CloudWatch alarms | < $0.20 |
| SNS | < $0.05 |
| DynamoDB on-demand | < $0.05 |
| Lambda | < $0.01 |
| **Session total (typical)** | **≈ $0.50 – $2.00** |

If a KMS CMK remains in PendingDeletion for 7 days, expect roughly **~$1/month prorated** until deletion completes—still destroy promptly.

---

## Optional CRR scenario (higher cost)

Assumptions: `enable_replication = true`, few hundred MB replicated, left running **24 hours**.

| Extra cost driver | Rough impact |
| ----------------- | ------------ |
| Dual-region storage | Storage × 2 + replication data transfer |
| Replication requests | Small at lab scale |
| Forgotten overnight | Can surprise students |

**Guidance:** Enable CRR only for stretch learning and destroy within hours. Prefer **simulated DR runbook** for core credit.

---

## Budget alert recommendation

Create an AWS Budget with alert at **$10** (actual) for the lab week, filterable by tag `Module=07` if using cost allocation tags.

---

## Cleanup

```bash
./infrastructure/terraform/scripts/cleanup-lab07.sh
```

Confirm no residual buckets, tables, alarms, SNS topics, or Lambda functions with BayLearn Module 07 tags.
