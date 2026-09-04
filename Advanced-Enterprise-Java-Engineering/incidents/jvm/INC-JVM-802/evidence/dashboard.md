# Dashboard — pay-prod-east-2

**Window:** 2026-10-06 16:00 Pacific through 2026-10-08 14:50 Pacific  
**Source:** synthetic BayPay Grafana snapshot  
**Gate:** 1

## Heap / old generation

| Instant (Pacific) | east-1 heap used | east-1 old gen | east-2 heap used | east-2 old gen | east-2 full GC / 1h |
|---|---|---|---|---|---|
| 06 Oct 16:20 (3.8.2 start) | 470 MB | 205 MB | 488 MB | 212 MB | 0 |
| 07 Oct 08:00 | 482 MB | 218 MB | 790 MB | 610 MB | 1 |
| 07 Oct 20:15 | 475 MB | 214 MB | 1010 MB | 780 MB | 2 |
| 08 Oct 12:10 | 491 MB | 220 MB | 1288 MB | 1095 MB | 4 |
| 08 Oct 14:42 | 490 MB | 221 MB | **1420 / 1536 MB** | **1288 MB** | **7** |

east-2 old generation **does not return** after full collections. east-1 is flat across the same two days.

## GC / allocation (08 Oct 14:40 Pacific)

| Metric | east-1 | east-2 |
|---|---|---|
| Allocation rate | 42 MB/s | 55 MB/s |
| GC pause p99 (15m) | 16 ms | 84 ms |
| Young GC interval | 4.1 s | 3.6 s |
| Full / mixed that reclaim old gen | old gen stays ~220 MB | old gen stays ~1280 MB after collect |

Allocation rate is not the story that matches a 1.8 GB/s pause page. The retained old set is.

## HTTP / API

| Metric | east-1 14:42 | east-2 14:42 |
|---|---|---|
| `POST /api/v1/payments` p99 | 175 ms | 2.8 s (during GC / recycle) |
| HTTP 5xx on create (5m) | 0 | 11 (502 when replica left the pool) |
| In-flight HTTP | 7 | 19 |

## Database (baypay, writer)

| Metric | 14:42 |
|---|---|
| CPU | 18% |
| Hikari active / max on east-2 | 14 / 50 |
| Hikari pending | 0 |
| `idempotency_record` table rows (writer) | 2.1M (stable growth, both replicas share the table) |

## Other replicas

`pay-prod-east-1`: version **3.8.0**, heap used 470–495 MB for 48 hours, readiness UP.

`pay-prod-east-2`: version **3.8.2** since 16:10 Pacific on 06 Oct. Recycled at 12:04 and 13:51 Pacific on 08 Oct; heap used returned to ~520 MB and climbed again. Liveness UP until each recycle.

## Notes

Avery Chen payment `c802d222-0000-4000-8000-111111111802` hit 502 on east-2 during the 13:51 recycle, then 201 on east-1 with the same `Idempotency-Key`.
