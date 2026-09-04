# INC-JVM-802 — Old generation climb on canary

**Lab:** INCIDENT-802  
**Severity:** SEV-2  
**Service:** payment-service (`pay-prod-east-2`)  
**When:** 2026-10-08 14:42 Pacific (21:42 UTC)  
**Data:** Synthetic BayPay. Not a real outage.

Evidence is **gated**. Follow `timeline.json` `gates`. Do not open later files to skip a hypothesis.

| Gate | When you may open it | File |
|---|---|---|
| 1 | After reading this page and the timeline | `evidence/dashboard.md` |
| 2 | After a written first hypothesis | `evidence/logs.txt` |
| 3 | After a written next investigation | `evidence/heap-histogram.md` |

Record work on [student-worksheet.md](student-worksheet.md).

This pack does not include a root-cause statement. Filenames and titles describe symptoms only.

## Evidence shipped versus omitted

The course catalog lists eleven evidence kinds. This pack is a **gated subset**, like INC-EE-402.

| Kind | In this pack? |
|---|---|
| Timeline | Yes — `timeline.json` |
| Dashboards | Yes — `evidence/dashboard.md` |
| Logs | Yes — `evidence/logs.txt` |
| Heap summary | Yes — `evidence/heap-histogram.md` (class histogram, not a full dump) |
| Thread dumps | **Omitted** |
| Deployment history | **Omitted** (version strings appear on the dashboard) |
| JVM metrics | **Omitted** as a standalone file (heap and GC appear on the dashboard) |
| Container metrics | **Omitted** |
| Database metrics | **Omitted** as a standalone file (a short DB row is on the dashboard) |
| Queue depth | **Omitted** |
| Dependency latency | **Omitted** |

If you believe you need an omitted kind, write *why* on the worksheet and what you expect it to show. Do not invent numbers.
