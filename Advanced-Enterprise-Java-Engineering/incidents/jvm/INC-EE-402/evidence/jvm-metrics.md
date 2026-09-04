# JVM metrics — pay-prod-east-2

**Captured:** 2026-08-14T21:14:00Z  
**Gate:** 3  
**Synthetic BayPay**

## Runtime

| Metric | Value |
|---|---|
| Heap used / max | 612 MB / 1536 MB |
| GC pause p99 (5m) | 18 ms |
| CPU process | 18% |
| Live threads | 214 |
| Blocked threads | 44 (name prefix `http-nio-8080-exec-`) |
| Waiting on | `com.zaxxer.hikari.pool.HikariPool.getConnection` (44 stacks sampled) |

## Hikari MXBean (same instant)

| Attribute | Value |
|---|---|
| TotalConnections | 50 |
| ActiveConnections | 50 |
| IdleConnections | 0 |
| ThreadsAwaitingConnection | 41 |
| MaxLifetime | 1800000 ms |
| LeakDetectionThreshold | 20000 ms |

## Threads of interest (sampled names)

```
http-nio-8080-exec-12  BLOCKED  HikariPool.getConnection
http-nio-8080-exec-19  BLOCKED  HikariPool.getConnection
settlement-preview-1   RUNNABLE java.sql.ResultSet.next
settlement-preview-1   (local frame) SettlementPreviewJob.streamOpenPayments
```

No `OutOfMemoryError`. Metaspace 89 MB / 256 MB, stable versus yesterday’s deploy.
