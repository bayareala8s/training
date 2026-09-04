# INC-WAS-502 — Cluster members stop processing

**Lab:** INCIDENT-502  
**Severity:** SEV-2  
**Service:** `payment.ear` on `PaymentCluster` (`BayPayCell`)  
**When:** 2026-09-08 14:16 Pacific (21:16 UTC)  
**Data:** Synthetic BayPay. Not a real outage.

Evidence is **gated**. Follow `timeline.json` `gates`. Do not open later files to skip a hypothesis.

| Gate | When you may open it | File |
|---|---|---|
| 1 | After reading this page and the timeline | `evidence/dashboard.md` |
| 2 | After a written first hypothesis | `evidence/logs.txt` |
| 3 | After a written next investigation | `evidence/plugin-status.md` |

Record work on [student-worksheet.md](student-worksheet.md).

This pack does not include a root-cause statement. Filenames and titles describe symptoms only.

## Evidence shipped versus omitted

The course catalog lists eleven evidence kinds. This pack is a **gated subset**, like INC-EE-402.

| Kind | In this pack? |
|---|---|
| Timeline | Yes — `timeline.json` |
| Dashboards | Yes — `evidence/dashboard.md` |
| Logs | Yes — `evidence/logs.txt` |
| IHS / plugin view | Yes — `evidence/plugin-status.md` (edge membership; not a separate catalog kind) |
| Thread dumps | **Omitted** |
| Heap summary | **Omitted** |
| Deployment history | **Omitted** |
| JVM metrics | **Omitted** (some thread-pool gauges appear on the dashboard) |
| Container metrics | **Omitted** (no containers in this estate) |
| Database metrics | **Omitted** as a standalone file (a short DB row is on the dashboard) |
| Queue depth | **Omitted** |
| Dependency latency | **Omitted** |

If you believe you need an omitted kind, write *why* on the worksheet and what you expect it to show. Do not invent numbers.
