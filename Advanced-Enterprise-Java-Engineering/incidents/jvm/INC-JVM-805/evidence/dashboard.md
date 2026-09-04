# Dashboard — pay-prod-east-2

**Window:** 2026-10-14 14:40–15:45 Pacific  
**Source:** synthetic BayPay Grafana snapshot  
**Gate:** 1

## GC / allocation

| Metric | east-1 15:40 | east-2 14:45 | east-2 15:10 | east-2 15:33 |
|---|---|---|---|---|
| Allocation rate | 38 MB/s | 44 MB/s | **1.6 GB/s** | **1.8 GB/s** |
| G1 pause p99 (5m) | 16 ms | 18 ms | 280 ms | **420 ms** |
| G1 pause max (5m) | 22 ms | 24 ms | 510 ms | **640 ms** |
| Young GC interval | 4.0 s | 3.8 s | **0.12 s** | **0.11 s** |
| Old gen used | 218 MB | 221 MB | 230 MB | 228 MB |
| Heap used (sawtooth max) | 520 MB | 535 MB | 980 MB | 1010 MB |
| Heap max | 1536 MB | 1536 MB | 1536 MB | 1536 MB |

Old generation is **flat**. Heap used rises and falls with young collections. This is not the two-day retained climb on the 3.8.2 cache pack.

## Logging / process

| Metric | east-1 15:40 | east-2 14:45 | east-2 15:33 |
|---|---|---|---|
| Log lines / s | 36 | 41 | **4200** |
| Process CPU | 12% | 14% | **71%** (GC + logging) |
| `logging.level.com.baypay` | INFO | INFO | **DEBUG** (runtime overlay) |

## HTTP / API

| Metric | east-1 15:40 | east-2 15:33 |
|---|---|---|
| `POST /api/v1/payments` p50 | 88 ms | 210 ms |
| `POST /api/v1/payments` p99 | 175 ms | **890 ms** |
| HTTP 5xx (5m) | 0 | 4 (client abandon) |
| Hikari active / max | 10 / 50 | 12 / 50 |

## Database

| Metric | 15:40 |
|---|---|
| CPU | 17% |
| Writer p99 | 13 ms |

## Other replicas

`pay-prod-east-1`: INFO, allocation 38 MB/s, pause p99 16 ms, Avery Chen create 201 at 15:35 Pacific without a stall.

`pay-prod-east-2`: DEBUG overlay since 14:50 Pacific (Jordan, BAYPAY-8055). Liveness UP. Readiness UP (pauses are long but probes still fit).

## Notes

Avery Chen payment `c805d555-0000-4000-8000-111111111805` completes; merchants feel the pause, not a 500.
