# Dashboard — PaymentCluster

**Window:** 2026-09-08 14:00–14:25 Pacific  
**Source:** synthetic BayPay operations snapshot (PMI + IHS access counters)  
**Gate:** 1

## Member state (admin console / node agent)

| Server | Node | State | `payment.ear` | HTTP 201 / 5m (14:20) | p99 `/payment` |
|---|---|---|---|---|---|
| `Pay1` | `node-pay-1` | STARTED | started | 184 | 210 ms |
| `Pay2` | `node-pay-2` | STARTED | started | **2** | **>12 s** (many still open) |
| `Pay3` | `node-pay-2` | STARTED | started | **0** | **>12 s** (many still open) |

`dmgr-east` and all three node agents report running. No install window on the change calendar.

## Web container (PMI, 14:22)

| Server | Active threads | Pool max | Hung-thread warnings / 10m | CPU |
|---|---|---|---|---|
| `Pay1` | 11 | 100 | 0 | 14% |
| `Pay2` | **100** | 100 | **47** | 6% |
| `Pay3` | **100** | 100 | **51** | 5% |

Pay2 and Pay3 sit at thread-pool ceiling with low CPU.

## JDBC `jdbc/baypay` (PMI, 14:22)

| Server | In use | Waiters | Max | PercentUsed |
|---|---|---|---|---|
| `Pay1` | 9 | 0 | 50 | 18% |
| `Pay2` | **50** | 41 | 50 | **100%** |
| `Pay3` | **50** | 38 | 50 | **100%** |

## Database (`db-east.baypay.example:5432` / `baypay`)

| Metric | 14:22 |
|---|---|
| CPU | 21% |
| `max_connections` | 400 |
| Sessions from `was-pay-1` | 9 |
| Sessions from `was-pay-2` | 50 (many idle in `idle in transaction` or awaiting client) |
| Writer availability | Up (blip 14:08–14:10 Pacific already cleared) |

## IHS counters (`ihs-east`)

| Backend | Requests / 5m | HTTP 5xx from backend / 5m | Connect failures |
|---|---|---|---|
| `Pay1:9080` | 190 | 0 | 0 |
| `Pay2:9080` | 188 | 71 (timeouts) | 0 |
| `Pay3:9081` | 181 | 80 (timeouts) | 0 |

Plugin connect failures remain zero. Traffic is still split across three members.

## Notes

Avery Chen create at 14:18 Pacific (payment `c502a111-0000-4000-8000-111111111502`) returned 201 on a retry after two timeouts. Harbor Market sees the pattern as “flaky network.”
