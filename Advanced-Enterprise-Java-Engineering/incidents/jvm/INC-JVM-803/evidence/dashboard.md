# Dashboard — pay-prod-east-2

**Window:** 2026-10-10 01:45–02:20 Pacific  
**Source:** synthetic BayPay Grafana snapshot  
**Gate:** 1

## HTTP / completions

| Metric | east-1 02:15 | east-2 01:55 | east-2 02:11 | east-2 02:15 |
|---|---|---|---|---|
| `POST /api/v1/payments` completed rps | 4.2 | 3.8 | **0.0** | **0.0** |
| `POST /api/v1/payments` p99 | 170 ms | 190 ms | (no completes) | (no completes) |
| In-flight HTTP creates | 5 | 7 | **46** | **61** |
| HTTP 5xx (5m) | 0 | 0 | 0 | 2 (client timeout) |
| Tomcat busy / max | 9 / 200 | 11 / 200 | 64 / 200 | 68 / 200 |

Creates on east-2 stop completing. Threads are still accepted.

## Process / JVM

| Metric | east-1 02:15 | east-2 02:15 |
|---|---|---|
| Process CPU | 11% | **4%** |
| Live threads | 122 | 148 |
| BLOCKED threads (sampled) | 0 | **22** |
| Heap used / max | 505 / 1536 MB | 498 / 1536 MB |
| GC pause p99 (15m) | 15 ms | 14 ms |

CPU is idle. Heap is quiet. This is not INCIDENT-801 or INCIDENT-802’s shape.

## Database / pool

| Metric | 02:15 |
|---|---|
| DB CPU | 16% |
| Hikari active / max on east-2 | 3 / 50 |
| Hikari pending | 0 |
| Sessions from east-2 | 3 (one named `nightly-reversal-1` idle in transaction 0) |

Pool exhaustion is not the page.

## Other replicas

`pay-prod-east-1`: version 3.8.0, nightly job **not** enabled, completions steady, Avery Chen retry 201 at 02:13 Pacific.

`pay-prod-east-2`: version 3.8.2, feature `nightly-reversal-job` enabled. Liveness UP. Readiness still UP (health check does not take application monitors).

## Notes

In-flight Avery Chen payment `c803d333-0000-4000-8000-111111111803` is 8+ minutes old on east-2.
