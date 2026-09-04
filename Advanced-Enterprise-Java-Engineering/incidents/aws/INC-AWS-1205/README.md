# INC-AWS-1205 — Failed ECS deploy after a green pipeline

**Lab:** INCIDENT-1205  
**Severity:** SEV-2  
**Service:** payment-service (`baypay-prod-west`, `us-west-2`)  
**When:** 2026-12-03 14:07 Pacific (22:07 UTC)  
**Data:** Synthetic BayPay. Not a real outage.

Evidence is **gated**. Follow `timeline.json` `gates`. Do not open later files to skip a hypothesis.

| Gate | When you may open it | File |
|---|---|---|
| 1 | After reading this page and the timeline | `evidence/pipeline.log` |
| 2 | After a written first hypothesis | `evidence/ecs-deployments.txt` |
| 3 | After a written next investigation | `evidence/task-def-diff.txt` |

Record work on [student-worksheet.md](student-worksheet.md).

This pack does not include a root-cause statement. Filenames and titles describe symptoms only.

## Evidence shipped versus omitted

The course catalog lists eleven evidence kinds. This pack is a **gated subset**, like INC-K8S-1006.

| Kind | In this pack? |
|---|---|
| Timeline | Yes — `timeline.json` |
| Pipeline / CI log | Yes — `evidence/pipeline.log` |
| ECS deployments | Yes — `evidence/ecs-deployments.txt` |
| Task definition diff | Yes — `evidence/task-def-diff.txt` |
| Application logs.txt | **Omitted** |
| ALB access logs | **Omitted** (health status appears on the deployment paste) |
| Dashboards | **Omitted** |
| Thread dumps | **Omitted** |
| Database metrics | **Omitted** |
| VPC / security groups | **Omitted** |
| Secrets Manager values | **Omitted** — do not invent `BAYPAY_DB_*` |

If you believe you need an omitted kind, write *why* on the worksheet and what you expect it to show. Do not invent numbers.
