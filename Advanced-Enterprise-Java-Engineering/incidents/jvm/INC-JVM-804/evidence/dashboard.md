# Dashboard — pay-prod-east-2

**Window:** 2026-10-13 10:40–11:20 Pacific  
**Source:** synthetic BayPay Grafana snapshot  
**Gate:** 1

## Tomcat / HTTP

| Metric | east-1 11:12 | east-2 10:55 | east-2 11:07 | east-2 11:12 |
|---|---|---|---|---|
| `tomcat_threads_busy` / max | 11 / 200 | 48 / 200 | **200 / 200** | **200 / 200** |
| `tomcat_threads_config_max` | 200 | 200 | 200 | 200 |
| Accept queue | 0 | 4 | **80** | **96** |
| `POST /api/v1/payments` p99 | 185 ms | 2.4 s | **12.1 s** | **12.4 s** |
| HTTP 5xx / 504 (5m) | 0 | 3 | 41 | 55 |
| In-flight HTTP | 8 | 51 | 200 | 200 |

Inbound workers are at the cap. New sockets sit in the accept queue.

## Hikari / database

| Metric | 11:12 |
|---|---|
| DB CPU | **15%** |
| Hikari active / max on east-2 | **8 / 50** |
| Hikari pending | 0 |
| Hikari timeouts (5m) | 0 |
| Sessions from east-1 | 10 |

This is not INC-EE-402. The database is not the waiter.

## Downstream

| Target | east-1 p99 | east-2 10:50 p99 | east-2 11:12 p99 |
|---|---|---|---|
| `fx-east.baypay.example` `/quote` | 38 ms | 41 ms | **no success samples** (in-flight 8) |
| baypay writer | 12 ms | 14 ms | 13 ms |

`fx-east` probe from the SRE jump host: connect succeeds, HTTP GET `/quote` exceeds 30s.

## Other replicas

`pay-prod-east-1`: version 3.8.0, `fx-quote-on-create` **off**, Tomcat 9–12 / 200, Avery Chen retry 201.

`pay-prod-east-2`: version 3.8.2, `fx-quote-on-create` **on**. Liveness UP. Readiness failed at 11:08 and 11:11 (`http` component: no free worker).

## Notes

Avery Chen payment `c804d444-0000-4000-8000-111111111804` is USD on account `22222222-2222-2222-2222-222222222221`. The canary still calls FX for a preview field.
