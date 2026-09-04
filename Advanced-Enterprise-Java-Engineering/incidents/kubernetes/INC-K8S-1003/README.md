# INC-K8S-1003 — Ingress 503 while payment pods stay Running

**Lab:** INCIDENT-1003  
**Severity:** SEV-2  
**Service:** payment-service (`baypay-prod`)  
**When:** 2026-11-10 09:40 Pacific (17:40 UTC)  
**Data:** Synthetic BayPay. Not a real outage.

Evidence is **gated**. Follow `timeline.json` `gates`. Do not open later files to skip a hypothesis.

| Gate | When you may open it | File |
|---|---|---|
| 1 | After reading this page and the timeline | `evidence/describe.txt` |
| 2 | After a written first hypothesis | `evidence/endpoints.txt` |
| 3 | After a written next investigation | `evidence/curl-ingress.txt` |

Record work on [student-worksheet.md](student-worksheet.md).

This pack does not include a root-cause statement. Filenames and titles describe symptoms only.

## Evidence shipped versus omitted

The course catalog lists eleven evidence kinds. This pack is a **gated subset**, like INC-EE-402.

| Kind | In this pack? |
|---|---|
| Timeline | Yes — `timeline.json` |
| Container describe | Yes — `evidence/describe.txt` |
| Service Endpoints | Yes — `evidence/endpoints.txt` |
| Ingress curl | Yes — `evidence/curl-ingress.txt` |
| Application logs.txt | **Omitted** |
| Dashboards | **Omitted** |
| Thread dumps | **Omitted** |
| Deployment history | **Omitted** (an image/probe change appears in the timeline) |
| Database metrics | **Omitted** |
| Queue depth | **Omitted** |
| TLS / openssl | **Omitted** (handshake is not the first complaint) |

If you believe you need an omitted kind, write *why* on the worksheet and what you expect it to show. Do not invent numbers.
