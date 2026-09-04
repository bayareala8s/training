# INC-K8S-1006 — Ingress 503 with empty Service endpoints

**Lab:** INCIDENT-1006  
**Severity:** SEV-2  
**Service:** payment-service (`baypay-prod`)  
**When:** 2026-11-19 11:33 Pacific (19:33 UTC)  
**Data:** Synthetic BayPay. Not a real outage.

Evidence is **gated**. Follow `timeline.json` `gates`. Do not open later files to skip a hypothesis.

| Gate | When you may open it | File |
|---|---|---|
| 1 | After reading this page and the timeline | `evidence/service.yaml` |
| 2 | After a written first hypothesis | `evidence/deploy-labels.yaml` |
| 3 | After a written next investigation | `evidence/endpoints.txt` |

Record work on [student-worksheet.md](student-worksheet.md).

This pack does not include a root-cause statement. Filenames and titles describe symptoms only.

## Evidence shipped versus omitted

The course catalog lists eleven evidence kinds. This pack is a **gated subset**, like INC-EE-402.

| Kind | In this pack? |
|---|---|
| Timeline | Yes — `timeline.json` |
| Service YAML | Yes — `evidence/service.yaml` |
| Deployment labels | Yes — `evidence/deploy-labels.yaml` |
| Service Endpoints | Yes — `evidence/endpoints.txt` |
| Application logs.txt | **Omitted** |
| Container describe / probes | **Omitted** (use labels + Endpoints; contrast INC-K8S-1003) |
| Dashboards | **Omitted** |
| Thread dumps | **Omitted** |
| Deployment history | **Omitted** (a label cleanup appears in the timeline) |
| Database metrics | **Omitted** |
| TLS / openssl | **Omitted** |

If you believe you need an omitted kind, write *why* on the worksheet and what you expect it to show. Do not invent numbers.
