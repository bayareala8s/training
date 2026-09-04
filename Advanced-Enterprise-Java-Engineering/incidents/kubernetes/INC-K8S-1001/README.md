# INC-K8S-1001 — Payment pods CrashLoopBackOff in baypay-prod

**Lab:** INCIDENT-1001  
**Severity:** SEV-2  
**Service:** payment-service (`baypay-prod`)  
**When:** 2026-11-03 10:22 Pacific (18:22 UTC)  
**Data:** Synthetic BayPay. Not a real outage.

Evidence is **gated**. Follow `timeline.json` `gates`. Do not open later files to skip a hypothesis.

| Gate | When you may open it | File |
|---|---|---|
| 1 | After reading this page and the timeline | `evidence/describe.txt` |
| 2 | After a written first hypothesis | `evidence/logs.txt` |
| 3 | After a written next investigation | `evidence/configmap.yaml` |

Record work on [student-worksheet.md](student-worksheet.md).

This pack does not include a root-cause statement. Filenames and titles describe symptoms only.

## Evidence shipped versus omitted

The course catalog lists eleven evidence kinds. This pack is a **gated subset**, like INC-EE-402.

| Kind | In this pack? |
|---|---|
| Timeline | Yes — `timeline.json` |
| Container describe | Yes — `evidence/describe.txt` |
| Application logs.txt | Yes — `evidence/logs.txt` |
| ConfigMap excerpt | Yes — `evidence/configmap.yaml` |
| Dashboards | **Omitted** |
| Thread dumps | **Omitted** (process may never finish start) |
| Heap histogram | **Omitted** |
| Deployment revision history | **Omitted** (a roll appears in the timeline) |
| Database metrics | **Omitted** |
| Queue depth | **Omitted** |
| Dependency latency | **Omitted** |

If you believe you need an omitted kind, write *why* on the worksheet and what you expect it to show. Do not invent numbers.
