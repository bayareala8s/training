# INC-JVM-201 — Duplicate payments under concurrency

**Lab:** BREAKFIX-201  
**Severity:** SEV-2  
**Service:** baypay-payment-canary (fictional)  
**When:** 2026-08-18 (Saturday sale)

BayPay is fictional. Every id, name, and metric below is synthetic.

## How to request evidence

Do not open every file in `evidence/` at the start. Work this order and write on [student-worksheet.md](student-worksheet.md) after each step.

| Step | Request | File | What you should record |
|---|---|---|---|
| 0 | Timeline | [timeline.json](timeline.json) | When pages fired, who was on call |
| 1 | Dashboard | [evidence/dashboard.md](evidence/dashboard.md) | Throughput, error rate, duplicate counter |
| 2 | Logs | [evidence/logs.txt](evidence/logs.txt) | Correlation ids, keys, post counts |
| 3 | Next | Your call | What you would request if this were live (`jstack`, heap, DB, deploy) |

Later evidence kinds (thread dump, heap summary, deploy history, JVM/container/DB metrics, queue depth, dependency latency) are **not** in this pack on purpose. If you believe you need one, write *why* on the worksheet and what you expect it to show. Do not invent numbers.

The instructor pack is `solutions/BREAKFIX-201/`. It is not evidence.

## Rules

- One hypothesis at a time. Update it; do not stack five untested theories.
- Quote a line of evidence under every claim.
- Stabilize vs remediate vs comms are separate boxes.
- A guess that later matches the solution file does not replace steps 0–2.
