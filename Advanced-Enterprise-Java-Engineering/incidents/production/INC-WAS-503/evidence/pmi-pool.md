# PMI — jdbc/baypay and web container

**Captured:** 2026-09-15T17:48:00Z  
**Cell:** `BayPayCell`  
**Scope:** per application server (not a cell-wide single counter)  
**Gate:** 3  
**Synthetic BayPay**

## DataSource `jdbc/baypay` (J2C connection pool)

Definition: cell-scoped, `maxConnections = 50`, J2C alias `baypayDbAlias`.  
`jdbc/baypayXA` is not in use on these members this morning.

| Server | CreateCount | CloseCount | AllocateCount | PercentUsed | PoolSize | WaitTime (ms, last) | WaitingThreadCount |
|---|---|---|---|---|---|---|---|
| `Pay1` | 50 | 0 (since 09:55) | 1844 | **100** | **50** | 180000 | **36** |
| `Pay2` | 18 | 7 | 640 | 22 | 18 | 0 | 0 |
| `Pay3` | 16 | 6 | 611 | 20 | 16 | 0 | 0 |

Pay1: **50 in use / 50 max**. Waiters stay high. Closes since `reporting.ear` start are zero — checkouts are not returning.

## Who is allocated on Pay1 (connection leak / holder trace, PMI + J2C)

| Thread name | Application | Connections held | Oldest checkout |
|---|---|---|---|
| `reporting-preview-1` | `reporting.ear` | 14 | 28 min |
| `reporting-preview-2` | `reporting.ear` | 9 | 21 min |
| `WebContainer : *` (sum) | `payment.ear` | 27 | 3 min (most blocked in allocate) |

Reporting holds **23** of 50. Payment HTTP threads hold or wait for the rest. No refund threads on this JVM.

## Web container (Pay1)

| Metric | Value |
|---|---|
| Active threads | 63 / 100 |
| Threads in `createOrWaitForConnection` | 36 |
| Hung-thread warnings / 20m | 2 (both over 10 min, reporting preview — not interrupted) |
| Heap used / max | 704 MB / 1536 MB |
| GC pause p99 (10m) | 22 ms |

Heap is not the constraint.

## Validation settings (Pay1 DataSource custom properties)

| Property | Value |
|---|---|
| `preTestSQLString` | (unset) |
| `testConnection` | false |
| `agedTimeout` | 0 |
| `unusedTimeout` | 1800 |
| `connLeakReclaim` | false |

## Notes

Morgan Hale: “I can stop `reporting.ear` on `Pay1` without uninstalling `payment.ear`. I have not done that yet.”  
Riley Okonkwo: “Do not raise max to 200 until we know who holds the 50.”
