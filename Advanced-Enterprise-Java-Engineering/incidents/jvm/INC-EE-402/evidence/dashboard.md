# Dashboard — pay-prod-east-2

**Window:** 2026-08-14 13:50–14:20 Pacific  
**Source:** synthetic BayPay Grafana snapshot  
**Gate:** 1

## HikariPool baypay-payment

| Metric | 13:55 | 14:05 | 14:12 |
|---|---|---|---|
| `hikaricp_connections_max` | 50 | 50 | 50 |
| `hikaricp_connections_active` | 12 | **50** | **50** |
| `hikaricp_connections_idle` | 8 | 0 | 0 |
| `hikaricp_connections_pending` | 0 | 27 | **41** |
| `hikaricp_connections_timeout_total` (delta / 5m) | 0 | 18 | 64 |

In-use is **50/50** from 14:05. Waiters stay high.

## HTTP / API

| Metric | 13:55 | 14:12 |
|---|---|---|
| `POST /api/v1/payments` p99 | 180 ms | 8.6 s |
| HTTP 5xx on create (5m) | 0 | 51 |
| In-flight HTTP requests | 14 | 73 |

## Database (baypay, writer)

| Metric | 14:12 |
|---|---|
| CPU | 19% |
| Active sessions from `pay-prod-east-2` | 50 |
| `max_connections` | 400 |
| Slow query (>2s) count / 5m | 1 (settlement preview, 48s elapsed, still running) |

## Other replicas

`pay-prod-east-1` and `pay-prod-east-3`: active connections 9–14 / 50, pending 0, p99 160–220 ms.

## Notes

Readiness on `pay-prod-east-2` failed two probes at 14:07 and 14:11 (`db` component timed out). Liveness remained UP.
