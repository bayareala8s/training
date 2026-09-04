# INC-JVM-202 — Payment and refund workers not completing

**Lab:** INCIDENT-202  
**Severity:** SEV-2  
**Service:** baypay-payment-canary (fictional)  
**When:** 2026-08-21

BayPay is fictional. Every id, name, dump line, and metric below is synthetic.

## How to request evidence

Do not open every file in `evidence/` at the start. Work this order and write on [student-worksheet.md](student-worksheet.md) after each step.

| Step | Request | File | What you should record |
|---|---|---|---|
| 0 | Timeline | [timeline.json](timeline.json) | When completions dropped, who paged |
| 1 | Dashboard | [evidence/dashboard.md](evidence/dashboard.md) | Throughput, queue, CPU, health |
| 2 | Logs | [evidence/logs.txt](evidence/logs.txt) | Last successful posts, then silence |
| 3 | Thread dump | [evidence/thread-dump.txt](evidence/thread-dump.txt) | Who is waiting, who owns what |

Optional later kinds (heap, deploy history, container/DB metrics, dependency latency) are not in this pack. If you need one, write *why* and what you expect. Do not invent a GC death spiral that the dashboard contradicts.

The instructor pack is `solutions/INCIDENT-202/`. It is not evidence.

## Rules

- Hypothesis v1 must be written **before** you open the thread dump.
- Quote stacks; do not paraphrase the dump into a slogan.
- Stabilization (restore completions) is not the same as remediation (keep the next deploy safe).
- Communication updates must not invent a cause you have not evidenced.
- A lucky guess, including one inspired by a lab title, does not max Diagnostic method.
