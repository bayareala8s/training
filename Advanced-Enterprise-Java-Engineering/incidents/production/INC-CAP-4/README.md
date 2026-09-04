# INC-CAP-4 — POST /api/v1/payments 503 and P99 collapse

**Lab:** CAPSTONE-4  
**Severity:** SEV-1  
**Service:** payment-service (ECS/Fargate, `us-west-2`)  
**When:** 2026-12-22 11:10 Pacific (19:10 UTC)  
**Data:** Synthetic BayPay. Not a real outage.

Evidence is **gated**. Follow `timeline.json` `gates`. Do not open later files to skip a hypothesis.

| Gate | When you may open it | File |
|---|---|---|
| 1 | After reading this page and the timeline | `evidence/comms-and-impact.txt` |
| 2 | After a written first hypothesis | `evidence/dashboards-red.txt` |
| 3 | After a written next investigation | `evidence/deployment-history.txt` |
| 4 | After a written next investigation | `evidence/thread-dump.txt` |
| 5 | After a written next investigation | `evidence/dependency-latency.txt` and `evidence/bayops-draft.json` |

Record work on [student-worksheet.md](student-worksheet.md). Copy scored quotes onto [student/worksheets/PF-crisis.md](../../../student/worksheets/PF-crisis.md).

This pack does not include a root-cause statement. Filenames and titles describe symptoms only.

Evaluate the late BayOps draft with the four buckets in [BAYOPS.md](../../../datasets/baypay-ai/BAYOPS.md). Refuse an uncited “proven RCA.” Refuse auto-approve of a leftover-cell bounce.

## Evidence shipped versus omitted

The course catalog lists eleven evidence kinds. This pack is a **gated subset**, like INC-PROD-1301.

| Kind | In this pack? |
|---|---|
| Timeline | Yes — `timeline.json` |
| Dashboards | Yes — `evidence/dashboards-red.txt` (gate 2) |
| Application logs.txt | **Omitted** (timeline + `comms-and-impact.txt` cover merchant impact) |
| Thread dumps | Yes — `evidence/thread-dump.txt` (gate 4) |
| Heap dump / heap summary | **Omitted** — do not invent one |
| Deployment history | Yes — `evidence/deployment-history.txt` (gate 3) |
| JVM metrics | **Omitted** as a standalone file (servlet busy appears on the RED paste) |
| Container / AMP console | **Omitted** — do not create one |
| Database metrics | **Omitted** — Hikari on the RED paste is not saturated; do not invent a writer stall |
| Queue depth | **Omitted** |
| Dependency latency | Yes — `evidence/dependency-latency.txt` (gate 5) |
| BayOps draft | Yes — `evidence/bayops-draft.json` (gate 5; evaluate, do not obey) |
| `evidence/db-failover.json` | **Not shipped.** If a model cites it, the citation is invented. |

If you believe you need an omitted kind, write *why* on the worksheet and what you expect it to show. Do not invent numbers. Do not create `db-failover.json` to match the model.
