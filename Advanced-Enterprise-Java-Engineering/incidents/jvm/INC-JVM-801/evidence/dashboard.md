# Dashboard — pay-prod-east-2

**Window:** 2026-10-06 09:50–10:30 Pacific  
**Source:** synthetic BayPay Grafana snapshot  
**Gate:** 1

## Process / JVM

| Metric | east-1 (3.8.0) | east-2 10:05 | east-2 10:18 | east-2 10:24 |
|---|---|---|---|---|
| Process CPU | 12% | 41% | **98%** | **97%** |
| Load average (1m) | 0.4 | 1.8 | 3.9 | 3.8 |
| Live threads | 118 | 142 | 168 | 171 |
| Heap used / max | 480 / 1536 MB | 512 / 1536 MB | 540 / 1536 MB | 528 / 1536 MB |
| GC pause p99 (5m) | 14 ms | 16 ms | 19 ms | 18 ms |
| Old gen used | 210 MB | 218 MB | 224 MB | 221 MB |

Heap is not climbing. GC pauses stay short. The page is CPU, not pause time.

## HTTP / API

| Metric | east-1 10:24 | east-2 10:05 | east-2 10:24 |
|---|---|---|---|
| `POST /api/v1/payments` p50 | 90 ms | 210 ms | 3.4 s |
| `POST /api/v1/payments` p99 | 180 ms | 1.1 s | **9.4 s** |
| HTTP 5xx on create (5m) | 0 | 2 | 28 |
| In-flight HTTP requests | 6 | 19 | **74** |
| Tomcat busy / max | 8 / 200 | 22 / 200 | 81 / 200 |

## Database (baypay, writer)

| Metric | 10:24 |
|---|---|
| CPU | 17% |
| Active sessions from `pay-prod-east-2` | 11 |
| Active sessions from `pay-prod-east-1` | 9 |
| Hikari active / max on east-2 | 11 / 50 |
| Hikari pending on east-2 | 0 |

This is not a 50/50 pool page.

## Other replicas

`pay-prod-east-1`: version **3.8.0**, CPU 11–13%, p99 160–200 ms, readiness UP for the whole window.

`pay-prod-east-2`: version **3.8.1** (canary since 09:40 Pacific). Readiness failed two probes at 10:19 and 10:22 (`http` component slow). Liveness remained UP.

## Notes

Load balancer still sends ~15% of `POST /api/v1/payments` to east-2. Avery Chen payment `c801d111-0000-4000-8000-111111111801` shows one hung attempt on east-2 and a later 201 on east-1.
