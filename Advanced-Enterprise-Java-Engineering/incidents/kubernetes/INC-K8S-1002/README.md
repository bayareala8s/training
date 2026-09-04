# INC-K8S-1002 — Payment pods OOMKilled after memory change

**Lab:** INCIDENT-1002  
**Severity:** SEV-2  
**Service:** payment-service (`baypay-prod`)  
**When:** 2026-11-05 15:10 Pacific (23:10 UTC)  
**Data:** Synthetic BayPay. Not a real outage.

Evidence is **gated**. Follow `timeline.json` `gates`. Do not open later files to skip a hypothesis.

| Gate | When you may open it | File |
|---|---|---|
| 1 | After reading this page and the timeline | `evidence/describe.txt` |
| 2 | After a written first hypothesis | `evidence/events.txt` |
| 3 | After a written next investigation | `evidence/jvm-flags.txt` |

Record work on [student-worksheet.md](student-worksheet.md).

This pack does not include a root-cause statement. Filenames and titles describe symptoms only.

## Evidence shipped versus omitted

The course catalog lists eleven evidence kinds. This pack is a **gated subset**, like INC-JVM-806, with kube describe as gate 1.

| Kind | In this pack? |
|---|---|
| Timeline | Yes — `timeline.json` |
| Container describe | Yes — `evidence/describe.txt` |
| Container / kube events | Yes — `evidence/events.txt` |
| JVM flags / last state | Yes — `evidence/jvm-flags.txt` |
| Application logs.txt | **Omitted** |
| Dashboards | **Omitted** (use describe + events) |
| Thread dumps | **Omitted** |
| Heap histogram | **Omitted** |
| Deployment history | **Omitted** (a limit change appears in the timeline) |
| Database metrics | **Omitted** |
| Queue depth | **Omitted** |

If you believe you need an omitted kind, write *why* on the worksheet and what you expect it to show. Do not invent numbers. Do not reuse INC-JVM-806 figures unless they appear here.
