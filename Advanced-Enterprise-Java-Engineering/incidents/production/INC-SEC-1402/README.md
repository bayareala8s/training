# INC-SEC-1402 — HTTPS handshake failures while payment tasks stay RUNNING

**Lab:** INCIDENT-1402  
**Severity:** SEV-2  
**Service:** payment-service (ECS/Fargate, `us-west-2`)  
**When:** 2026-09-02 00:15 Pacific (07:15 UTC)  
**Data:** Synthetic BayPay. Not a real outage.

Evidence is **gated**. Follow `timeline.json` `gates`. Do not open later files to skip a hypothesis.

| Gate | When you may open it | File |
|---|---|---|
| 1 | After reading this page and the timeline | `evidence/tls-handshake.txt` |
| 2 | After a written first hypothesis | `evidence/acm-describe.txt` |
| 3 | After a written next investigation | `evidence/route53-records.txt` |

Record work on [student-worksheet.md](student-worksheet.md).

This pack does not include a root-cause statement. Filenames and titles describe the investigation path and symptoms only.

No private keys are shipped. Do not request ACM or change Route 53 in a paid account.

## Evidence shipped versus omitted

The course catalog lists eleven evidence kinds. This pack is a **gated subset**, like INC-AWS-1104.

| Kind | In this pack? |
|---|---|
| Timeline | Yes — `timeline.json` |
| Client TLS / openssl-style handshake | Yes — `evidence/tls-handshake.txt` |
| ACM describe | Yes — `evidence/acm-describe.txt` |
| Route 53 records | Yes — `evidence/route53-records.txt` |
| Application logs.txt | **Omitted** (handshake may never reach Spring) |
| ECS describe / task health | **Omitted** as a standalone file (timeline says tasks RUNNING) |
| Security-group describe | **Omitted** |
| Dashboards | **Omitted** |
| Thread dumps | **Omitted** |
| Deployment history | **Omitted** |
| Database metrics | **Omitted** |
| Kubernetes TLS Secret | **Omitted** |

If you believe you need an omitted kind, write *why* on the worksheet and what you expect it to show. Do not invent numbers. Do not generate a real certificate.
