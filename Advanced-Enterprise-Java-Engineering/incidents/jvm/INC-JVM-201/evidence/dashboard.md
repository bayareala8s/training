# INC-JVM-201 dashboard (synthetic)

**Window:** 2026-08-18 17:50–18:30 UTC  
**Source:** fictional BayPay Grafana board `pay-canary-sale`  
**Host:** `sale-canary-1`

This file is evidence. It does not state a root cause.

## Golden signals

| Metric | 17:50–18:10 | 18:12–18:30 | Notes |
|---|---|---|---|
| Authorize throughput (rps) | 80–110 | 240–310 | Sale start 18:12 |
| HTTP 5xx ratio | 0.1% | 0.2% | Not paging |
| HTTP 201 ratio | 98% | 97% | Still “successful” |
| p50 authorize latency | 18 ms | 22 ms | In-process canary, no card I/O |
| p99 authorize latency | 45 ms | 70 ms | Slight rise, not a hang |
| CPU | 22% | 41% | Cores busy, not idle |
| Heap used | 512 MB / 1 GB | 548 MB / 1 GB | No GC death spiral |
| `/actuator/health` | UP | UP | |

## Payment-specific

| Metric | 17:50–18:10 | 18:12–18:30 |
|---|---|---|
| `duplicate_payment_ratio` (posts / distinct keys − 1, 5m) | 0.02% | **1.8%** |
| `ledger_minus_auth_count` (5m abs) | 0–2 | **40–90** |
| Distinct `Idempotency-Key` / min | 4,800 | 14,200 |
| Journal appends / min | 4,801 | 15,100 |
| In-flight canary threads | 8 | 8 |
| JDBC commit rate | 0 | 0 |

JDBC commit rate 0 is expected: this canary does not persist.

## Notes from the board

- Duplicate ratio is computed by the canary as `journal_rows_for_key > 1` sampled on a 1% of keys plus a merchant-reported counter.
- Harbor Bike Co key `harbor-8841` is in the extra-row sample (see logs).
- No saturation alert on the 8 worker threads.
- Queue depth for posting is near zero — work is completing, sometimes more than once.

## What this dashboard does not show

Thread identity of two posters for the same key, SQL, or a heap histogram. Request logs next.
