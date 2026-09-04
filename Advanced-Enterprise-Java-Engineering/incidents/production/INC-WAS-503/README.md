# INC-WAS-503 — JDBC pool exhaustion on ND

**Lab:** INCIDENT-503  
**Severity:** SEV-2  
**Service:** `payment.ear` on `PaymentCluster` (`BayPayCell`)  
**When:** 2026-09-15 10:41 Pacific (17:41 UTC)  
**Data:** Synthetic BayPay. Not a real outage.

Evidence is **gated**. Follow `timeline.json` `gates`. Do not open later files to skip a hypothesis.

| Gate | When you may open it | File |
|---|---|---|
| 1 | After reading this page and the timeline | `evidence/dashboard.md` |
| 2 | After a written first hypothesis | `evidence/logs.txt` |
| 3 | After a written next investigation | `evidence/pmi-pool.md` |

Record work on [student-worksheet.md](student-worksheet.md).

This pack does not include a root-cause statement. Filenames and titles describe symptoms only.

## Evidence shipped versus omitted

The course catalog lists eleven evidence kinds. This pack is a **gated subset**, like INC-EE-402.

| Kind | In this pack? |
|---|---|
| Timeline | Yes — `timeline.json` |
| Dashboards | Yes — `evidence/dashboard.md` |
| Logs | Yes — `evidence/logs.txt` |
| PMI pool snapshot | Yes — `evidence/pmi-pool.md` (JDBC / thread gauges; not a full JVM metrics dump) |
| Thread dumps | **Omitted** |
| Heap summary | **Omitted** |
| Deployment history | **Omitted** as a standalone file (install notes appear in the timeline and logs) |
| JVM metrics | **Omitted** (heap/CPU only as dashboard rows) |
| Container metrics | **Omitted** |
| Database metrics | **Omitted** as a standalone file (CPU and session counts are on the dashboard) |
| Queue depth | **Omitted** |
| Dependency latency | **Omitted** |

If you believe you need an omitted kind, write *why* on the worksheet and what you expect it to show. Do not invent numbers.
