# Cost Estimate — Lab 08 AI Decision Assistant

**Module:** 08  
**Case study:** NorthStar Financial Services (fictional)  
**Last updated:** 2026-07-15  
**Region assumption:** `us-east-1`

> **Cost warning:** Instructional estimates only. Always set a budget alert and run cleanup the same day.

---

## Design choices that keep cost low

| Choice | Effect |
| ------ | ------ |
| Mock Bedrock by default | Zero model token charges |
| Serverless (Lambda/SFN/API GW/DDB on-demand) | No idle compute |
| No NAT / EC2 / EKS / OpenSearch | Avoids large fixed costs |
| Short lab session | Limits request volume |

---

## Baseline scenario (mock mode, recommended)

Assumptions: ~2 hours, ≤50 decision invocations, cleanup same day.

| Service | Estimate |
| ------- | -------- |
| API Gateway HTTP | < $0.10 |
| Lambda | < $0.10 |
| Step Functions | < $0.20 |
| DynamoDB on-demand | < $0.05 |
| S3 | < $0.05 |
| CloudWatch | < $0.10 |
| **Session total (typical)** | **≈ $0.30 – $1.50** |

---

## Live Bedrock scenario

Assumptions: Nova Micro (or similar), ~20 eval incidents + retries, short prompts.

| Driver | Note |
| ------ | ---- |
| Input/output tokens | Dominates variable cost |
| Guardrails | Small additional charge if enabled |
| Forgotten overnight with traffic | Unlikely but cleanup still mandatory |

**Typical same-day live lab:** often still under **$5**, but depends on model and verbosity. Prefer mock until access is confirmed.

---

## Budget alert recommendation

AWS Budget alert at **$10** actual for the lab week; tag `Module=08`.

---

## Cleanup

```bash
./infrastructure/terraform/scripts/cleanup-lab08.sh
```
