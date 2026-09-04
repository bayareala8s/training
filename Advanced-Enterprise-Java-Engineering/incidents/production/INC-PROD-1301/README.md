# INC-PROD-1301 — Throughput collapse and P99 spike

**Lab:** INCIDENT-1301  
**Severity:** SEV-2  
**Service:** payment-service (`us-west-2`)  
**When:** 2026-12-18 10:22 Pacific (18:22 UTC)  
**Data:** Synthetic BayPay. Not a real outage.

Evidence is **gated**. Follow `timeline.json` `gates`. Do not open later files to skip a hypothesis.

| Gate | When you may open it | File |
|---|---|---|
| 1 | After reading this page and the timeline | `evidence/dashboards-red.txt` |
| 2 | After a written first hypothesis | `evidence/scrape-and-jvm.txt` |
| 3 | After a written next investigation | `evidence/meter-registration.txt` |

Record work on [student-worksheet.md](student-worksheet.md).

This pack does not include a root-cause statement. Filenames and titles describe symptoms only.

## Evidence shipped versus omitted

The course catalog lists eleven evidence kinds. This pack is a **gated subset**, like INC-AWS-1104.

| Kind | In this pack? |
|---|---|
| Timeline | Yes — `timeline.json` |
| Dashboards | Yes — `evidence/dashboards-red.txt` |
| JVM / scrape metrics | Yes — `evidence/scrape-and-jvm.txt` |
| Meter registration snippet | Yes — `evidence/meter-registration.txt` (gate 3) |
| Application logs.txt | **Omitted** (timeline + RED board cover merchant impact) |
| Thread dumps | **Omitted** — write what a dump would show if you wanted one; do not invent one |
| Heap dump / heap summary | **Omitted** — heap *used* appears as a number on the scrape/JVM paste; a dump is out of scope |
| Database metrics | **Omitted** — Hikari on the RED paste is not saturated; do not invent a writer stall |
| Deployment history (full) | **Omitted** as a standalone file (image 3.9.0 / ticket BAYPAY-13011 appear on the timeline) |
| Queue depth | **Omitted** |
| Dependency latency | **Omitted** |
| Container / AMP console | **Omitted** — do not create one |

If you believe you need an omitted kind, write *why* on the worksheet and what you expect it to show. Do not invent numbers.
