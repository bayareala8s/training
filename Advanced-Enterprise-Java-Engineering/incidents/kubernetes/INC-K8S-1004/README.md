# INC-K8S-1004 — Payment start failures after Secret update

**Lab:** INCIDENT-1004  
**Severity:** SEV-2  
**Service:** payment-service (`baypay-prod`)  
**When:** 2026-11-12 13:18 Pacific (21:18 UTC)  
**Data:** Synthetic BayPay. Not a real outage.

Evidence is **gated**. Follow `timeline.json` `gates`. Do not open later files to skip a hypothesis.

| Gate | When you may open it | File |
|---|---|---|
| 1 | After reading this page and the timeline | `evidence/secret-keys.txt` |
| 2 | After a written first hypothesis | `evidence/logs.txt` |
| 3 | After a written next investigation | `evidence/deployment-env.yaml` |

Record work on [student-worksheet.md](student-worksheet.md).

This pack does not include a root-cause statement. Filenames and titles describe symptoms only.

Secret **values** are redacted as `***`. Do not invent a password.

## Evidence shipped versus omitted

The course catalog lists eleven evidence kinds. This pack is a **gated subset**, like INC-EE-402.

| Kind | In this pack? |
|---|---|
| Timeline | Yes — `timeline.json` |
| Secret keys (names only) | Yes — `evidence/secret-keys.txt` |
| Application logs.txt | Yes — `evidence/logs.txt` |
| Deployment env YAML | Yes — `evidence/deployment-env.yaml` |
| Dashboards | **Omitted** |
| Thread dumps | **Omitted** |
| Heap histogram | **Omitted** |
| Full Secret YAML with data | **Omitted** (never shipped) |
| Database metrics | **Omitted** as a standalone file |
| Queue depth | **Omitted** |
| Dependency latency | **Omitted** |

If you believe you need an omitted kind, write *why* on the worksheet and what you expect it to show. Do not invent numbers. Do not decode Secret values.
