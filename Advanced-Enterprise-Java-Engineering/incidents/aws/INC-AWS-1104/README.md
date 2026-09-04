# INC-AWS-1104 — ALB 502/503 while payment tasks stay RUNNING

**Lab:** INCIDENT-1104  
**Severity:** SEV-2  
**Service:** payment-service (ECS/Fargate, `us-west-2`)  
**When:** 2026-11-12 14:10 Pacific (22:10 UTC)  
**Data:** Synthetic BayPay. Not a real outage.

Evidence is **gated**. Follow `timeline.json` `gates`. Do not open later files to skip a hypothesis.

| Gate | When you may open it | File |
|---|---|---|
| 1 | After reading this page and the timeline | `evidence/target-health.txt` |
| 2 | After a written first hypothesis | `evidence/task-def.json` |
| 3 | After a written next investigation | `evidence/alb-listener.txt` |

Record work on [student-worksheet.md](student-worksheet.md).

This pack does not include a root-cause statement. Filenames and titles describe symptoms only.

## Evidence shipped versus omitted

The course catalog lists eleven evidence kinds. This pack is a **gated subset**, like INC-K8S-1003.

| Kind | In this pack? |
|---|---|
| Timeline | Yes — `timeline.json` |
| Target health | Yes — `evidence/target-health.txt` |
| Task definition excerpt | Yes — `evidence/task-def.json` |
| ALB listener / curl | Yes — `evidence/alb-listener.txt` |
| Application logs.txt | **Omitted** |
| Security-group describe | **Omitted** (write what a timeout vs an HTTP code would show) |
| Dashboards | **Omitted** |
| Thread dumps | **Omitted** |
| Deployment history | **Omitted** (a target-group / task-def change appears in the timeline) |
| Database metrics | **Omitted** |
| VPC flow logs | **Omitted** |

If you believe you need an omitted kind, write *why* on the worksheet and what you expect it to show. Do not invent numbers.
