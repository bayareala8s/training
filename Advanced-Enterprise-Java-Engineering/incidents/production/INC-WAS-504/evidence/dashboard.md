# Dashboard — PaymentCluster during 4.12 window

**Window:** 2026-09-22 15:30–16:20 Pacific  
**Source:** synthetic BayPay operations snapshot  
**Gate:** 1

## Member health and edition (as reported by each JVM)

| Server | Node | State | `payment.ear` edition *on the member* | 2xx / 5m (16:12) | 5xx / 5m | p99 |
|---|---|---|---|---|---|---|
| `Pay1` | `node-pay-1` | STARTED | **4.12** | 22 | **61** | 420 ms |
| `Pay2` | `node-pay-2` | STARTED | **4.11** | 88 | 3 | 240 ms |
| `Pay3` | `node-pay-2` | STARTED | **4.11** | 84 | 2 | 255 ms |

Cell application view on `dmgr-east` lists `payment.ear` as **4.12**. That row does not match Pay2/Pay3.

## Error class (IHS + application, 16:05–16:15)

| Error | Count | Members seen on |
|---|---|---|
| `javax.naming.NameNotFoundException` | 54 | **Pay1 only** |
| Client timeout / 504 | 4 | mixed |
| Other 5xx | 8 | Pay2/Pay3 (retries after a Pay1 500) |

`jdbc/baypay` pool on all three members: in-use 8–14 / 50. This is not a 50/50 incident.

## Node agents and sync (console, 16:10 Pacific)

| Process | State | Last sync |
|---|---|---|
| `dmgr-east` | running | n/a (master) |
| `nodeagent-pay-1` | running | node-pay-1 **complete** at 15:46 |
| `nodeagent-pay-2` | running (restarted 15:47) | node-pay-2 **incomplete** — “repository copy interrupted” |
| `nodeagent-ref-1` | running | not targeted |

## Database

| Metric | 16:12 |
|---|---|
| CPU | 19% |
| Writer | Up |
| Unique violations / 10m | 0 |

## Notes

Avery Chen payment `c504d333-0000-4000-8000-111111111504`: first POST via `Pay1` returned 500; retry via `Pay2` returned 201. Same `Idempotency-Key`.
