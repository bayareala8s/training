# INC-JVM-803 — Payment creates hang after nightly window

**Lab:** INCIDENT-803  
**Severity:** SEV-2  
**Service:** payment-service (`pay-prod-east-2`)  
**When:** 2026-10-10 02:11 Pacific (09:11 UTC)  
**Data:** Synthetic BayPay. Not a real outage.

Evidence is **gated**. Follow `timeline.json` `gates`. Do not open later files to skip a hypothesis.

| Gate | When you may open it | File |
|---|---|---|
| 1 | After reading this page and the timeline | `evidence/dashboard.md` |
| 2 | After a written first hypothesis | `evidence/logs.txt` |
| 3 | After a written next investigation | `evidence/thread-dump.txt` |

Record work on [student-worksheet.md](student-worksheet.md).

This pack does not include a root-cause statement. Filenames and titles describe symptoms only.

This is **not** the INC-JVM-202 worker canary. Thread names and hosts in *this* dump are the evidence.

## Evidence shipped versus omitted

The course catalog lists eleven evidence kinds. This pack is a **gated subset**, like INC-EE-402.

| Kind | In this pack? |
|---|---|
| Timeline | Yes — `timeline.json` |
| Dashboards | Yes — `evidence/dashboard.md` |
| Logs | Yes — `evidence/logs.txt` |
| Thread dumps | Yes — `evidence/thread-dump.txt` |
| Heap summary | **Omitted** |
| Deployment history | **Omitted** |
| JVM metrics | **Omitted** as a standalone file (CPU and thread states appear on the dashboard) |
| Container metrics | **Omitted** |
| Database metrics | **Omitted** as a standalone file (a short DB row is on the dashboard) |
| Queue depth | **Omitted** |
| Dependency latency | **Omitted** |

If you believe you need an omitted kind, write *why* on the worksheet and what you expect it to show. Do not invent numbers.
