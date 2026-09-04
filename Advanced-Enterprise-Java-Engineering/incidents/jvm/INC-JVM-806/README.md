# INC-JVM-806 — Canary pod restarting

**Lab:** INCIDENT-806  
**Severity:** SEV-2  
**Service:** payment-service (`pay-prod-east-2`)  
**When:** 2026-10-15 16:48 Pacific (23:48 UTC)  
**Data:** Synthetic BayPay. Not a real outage.

Evidence is **gated**. Follow `timeline.json` `gates`. Do not open later files to skip a hypothesis.

| Gate | When you may open it | File |
|---|---|---|
| 1 | After reading this page and the timeline | `evidence/dashboard.md` |
| 2 | After a written first hypothesis | `evidence/kube-events.md` |
| 3 | After a written next investigation | `evidence/jvm-flags.md` |

Record work on [student-worksheet.md](student-worksheet.md).

This pack does not include a root-cause statement. Filenames and titles describe symptoms only.

## Evidence shipped versus omitted

The course catalog lists eleven evidence kinds. This pack is a **gated subset**, like INC-EE-402.

| Kind | In this pack? |
|---|---|
| Timeline | Yes — `timeline.json` |
| Dashboards | Yes — `evidence/dashboard.md` |
| Container / kube events | Yes — `evidence/kube-events.md` |
| JVM flags / last GC | Yes — `evidence/jvm-flags.md` |
| Application logs.txt | **Omitted** |
| Thread dumps | **Omitted** |
| Heap histogram | **Omitted** |
| Deployment history | **Omitted** (flag change appears in the timeline) |
| Database metrics | **Omitted** as a standalone file (a short DB row is on the dashboard) |
| Queue depth | **Omitted** |
| Dependency latency | **Omitted** |

If you believe you need an omitted kind, write *why* on the worksheet and what you expect it to show. Do not invent numbers.
