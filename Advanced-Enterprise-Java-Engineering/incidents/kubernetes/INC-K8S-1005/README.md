# INC-K8S-1005 — TLS handshake failures on payments host

**Lab:** INCIDENT-1005  
**Severity:** SEV-2  
**Service:** payment-service (`baypay-prod`)  
**When:** 2026-11-17 08:05 Pacific (16:05 UTC)  
**Data:** Synthetic BayPay. Not a real outage.

Evidence is **gated**. Follow `timeline.json` `gates`. Do not open later files to skip a hypothesis.

| Gate | When you may open it | File |
|---|---|---|
| 1 | After reading this page and the timeline | `evidence/ingress.yaml` |
| 2 | After a written first hypothesis | `evidence/openssl-dates.txt` |
| 3 | After a written next investigation | `evidence/curl-tls.txt` |

Record work on [student-worksheet.md](student-worksheet.md).

This pack does not include a root-cause statement. Filenames and titles describe symptoms only.

No private keys are shipped.

## Evidence shipped versus omitted

The course catalog lists eleven evidence kinds. This pack is a **gated subset**, like INC-EE-402.

| Kind | In this pack? |
|---|---|
| Timeline | Yes — `timeline.json` |
| Ingress YAML | Yes — `evidence/ingress.yaml` |
| openssl dates / subject | Yes — `evidence/openssl-dates.txt` |
| Client TLS curl | Yes — `evidence/curl-tls.txt` |
| Application logs.txt | **Omitted** (handshake may never reach Spring) |
| Container describe | **Omitted** as a standalone file (timeline says pods Ready) |
| Thread dumps | **Omitted** |
| Deployment history | **Omitted** |
| Database metrics | **Omitted** |
| Queue depth | **Omitted** |
| Secret tls.key | **Omitted** (never shipped) |

If you believe you need an omitted kind, write *why* on the worksheet and what you expect it to show. Do not invent numbers. Do not generate a real certificate.
