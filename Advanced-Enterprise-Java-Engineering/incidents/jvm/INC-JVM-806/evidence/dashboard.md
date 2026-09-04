# Dashboard — pay-prod-east-2

**Window:** 2026-10-15 15:10–17:00 Pacific  
**Source:** synthetic BayPay Grafana + teaching cluster snapshot  
**Gate:** 1

## Availability / restarts

| Instant (Pacific) | east-1 ready | east-2 ready | east-2 restarts (cumulative) | 502 / 5m (LB) |
|---|---|---|---|---|
| 15:20 (after resize) | yes | yes | 0 | 0 |
| 15:48 | yes | no (restarting) | 1 | 18 |
| 16:12 | yes | yes | 2 | 4 |
| 16:41 | yes | no (restarting) | 3 | 22 |
| 16:48 | yes | yes | **3** | 9 |

east-1 did not restart. Avery Chen 502s line up with east-2 leaving the pool.

## Process / memory (last good scrape before 16:41 kill)

| Metric | east-1 | east-2 |
|---|---|---|
| Pod / instance memory limit | 2Gi | **512Mi** |
| RSS (cgroup) | 890 MiB | **508 MiB** |
| Heap used / max | 510 / 1536 MB | **402 / 512 MB** |
| Metaspace used | 92 MB | 88 MB |
| Live threads | 124 | 131 |
| Direct buffer (est.) | 48 MB | 44 MB |
| Java `OutOfMemoryError` count | 0 | **0** |
| GC pause p99 (15m) | 16 ms | 22 ms |

Heap used on east-2 was **not** at 512 MB when RSS hit the cgroup. Last scrape: heap 402/512 MB, RSS 508 MiB.

## HTTP / API (when east-2 is up)

| Metric | east-1 16:50 | east-2 16:38 (pre-kill) |
|---|---|---|
| `POST /api/v1/payments` p99 | 180 ms | 210 ms |
| Hikari active / max | 11 / 50 | 10 / 50 |
| DB CPU | 16% | 16% |

## Other replicas

`pay-prod-east-1`: 2Gi limit, `-Xmx1536m`, no restarts, Avery Chen retry 201 for `c806d666-0000-4000-8000-111111111806`.

`pay-prod-east-2`: 512Mi canary since 15:15 Pacific (BAYPAY-8066). Liveness not observable during kill.

## Notes

No two-day old-gen climb in this window. The process does not live long enough for INCIDENT-802’s story.
