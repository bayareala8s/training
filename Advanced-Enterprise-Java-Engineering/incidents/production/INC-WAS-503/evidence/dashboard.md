# Dashboard — PaymentCluster and db-east

**Window:** 2026-09-15 09:50–10:50 Pacific  
**Source:** synthetic BayPay operations snapshot  
**Gate:** 1

## HTTP / payment API

| Member | 10:10 p99 `/payment` | 10:45 p99 | 201 / 5m (10:45) | 5xx / 5m |
|---|---|---|---|---|
| `Pay1` | 190 ms | **9.4 s** | 11 | **44** |
| `Pay2` | 180 ms | 230 ms | 96 | 0 |
| `Pay3` | 175 ms | 245 ms | 91 | 1 (client disconnect) |

`ihs-east` still balances across all three. Failures cluster on `was-pay-1.baypay.example`.

## Applications started (console, 10:44 Pacific)

| Server | Node | Ears started |
|---|---|---|
| `Pay1` | `node-pay-1` | `payment.ear`, **`reporting.ear`** (started 09:55 Pacific) |
| `Pay2` | `node-pay-2` | `payment.ear` |
| `Pay3` | `node-pay-2` | `payment.ear` |
| `Ref1` / `Ref2` | `node-ref-1` | `refund.ear` only |

## JDBC `jdbc/baypay` (PMI headline, 10:45)

| Server | In use | Waiters | Max | Timeout count / 10m |
|---|---|---|---|---|
| `Pay1` | **50** | **36** | 50 | 41 |
| `Pay2` | 11 | 0 | 50 | 0 |
| `Pay3` | 10 | 0 | 50 | 0 |
| `Ref1` | 3 | 0 | 50 | 0 |

Pay1 is **50/50**. Other payment members have spare connections.

## Database (`db-east.baypay.example:5432` / `baypay`)

| Metric | 10:45 |
|---|---|
| CPU | **17%** |
| Active sessions from `was-pay-1` | 50 |
| Active sessions from `was-pay-2` | 21 |
| `max_connections` | 400 |
| Slow query (>2s) count / 10m | 1 (`reporting` settlement preview, 11 minutes elapsed, still running) |
| Locks waiting | 0 |

Writer is accepting connections. Postgres is not at `max_connections`.

## Notes

Avery Chen payment `c503b222-0000-4000-8000-111111111503` failed on first POST (timeout via `Pay1`) and succeeded on retry via `Pay2` at 10:44 Pacific.
