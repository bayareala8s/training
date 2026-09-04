# INC-JVM-202 dashboard (synthetic)

**Window:** 2026-08-21 14:40–15:20 UTC  
**Source:** fictional BayPay Grafana board `pay-canary-weekday`  
**Host:** `sale-canary-1`  **pid:** 4412

This file is evidence. It does not state a root cause.

## Golden signals

| Metric | 14:40–15:03 | 15:04–15:20 | Notes |
|---|---|---|---|
| Payment completed rps | 18–24 | **0.0–0.4** | Drop starts 15:04:12 |
| Refund completed rps | 6–9 | **0.0** | Tracks the payment drop |
| HTTP accept rps | 30–40 | 28–35 | Clients still connect |
| In-flight HTTP > 30s | 0–1 | **22–28** | /payments and /refunds |
| HTTP 5xx ratio | 0.2% | 0.3% | Almost no errors — calls have not finished |
| p99 (completed requests only) | 40 ms | n/a | Few completions |
| CPU | 19% | **3–5%** | Idle, not pegged |
| Heap used | 490 MB / 1 GB | 501 MB / 1 GB | No allocation storm |
| GC pause p99 | 12 ms | 9 ms | Quiet |
| `/actuator/health` | UP | UP | |
| `/actuator/liveness` | UP | UP | |

## Queues and pools

| Metric | 14:40–15:03 | 15:04–15:20 |
|---|---|---|
| Posting queue depth | 0–4 | **180 → 640** and climbing |
| payment-worker threads | 8 | 8 (alive) |
| refund-worker threads | 4 | 4 (alive) |
| JDBC active connections | 0 | 0 |
| Outbound HTTP in-flight | 0 | 0 |
| Thread count (platform) | 62 | 64 |

## Notes from the board

- Completions for **both** payment and refund fall together.
- Workers exist; they are not exiting.
- CPU and GC do not look like a tight spin or a memory incident.
- Health/liveness do not take the posting path.
- JDBC and outbound HTTP are idle — this canary is in-process.

## What this dashboard does not show

Who owns which monitor. Request logs, then the thread dump.
