# INC-JVM-802 student worksheet

Fill in order. Quote evidence. Do not paste instructor solutions.

**Incident:** Old generation climb on canary  
**Instance:** `pay-prod-east-2` (canary) vs `pay-prod-east-1`  
**Your name / cohort:**  
**Time started:** 2026-09-06  
**Time submitted:** 2026-09-06

## Current hypothesis

(What do you think is happening? Update after each gate.)

Gate 1: SEV-2 is **`pay-prod-east-2` (3.8.2)** only. Old gen **212 → 1288 MB over ~46 hours** and **does not return** after full/mixed collects (stays ~1280 after collect). east-1 **3.8.0** old gen ~220 MB flat. Allocation 55 vs 42 MB/s — not an allocation-rate / pause page (INC-805 shape). Recycle at 12:04 and 13:51: heap drops to ~520 then **climbs again**. Avery 502 on recycle, 201 on east-1. Hikari 14/50 pending 0. This is a **growth / retained-set** story, not “the heap is full” and not “GC is broken.” First guess: 3.8.2 retains something per request (cache / map / ThreadLocal) that 3.8.0 does not. Next: logs (feature, sizes), then histogram — **which classes** dominate retained? Do not raise `-Xmx` as the cure. Do not bounce Postgres or `dmgr-east`.

Gate 2: Logs name an **unbounded in-process cache**, not a closed leak class yet. `IdempotencyReplayCache` **enabled=true maxSize=-1 ttlSeconds=0 backingMap=ConcurrentHashMap**. Size **184k → 1.10M** over two days; estimatedBytes **94 MB → 612 MB**. Hits stay far below size (never evicts). Feature `idempotency-replay-cache` on east-2 **3.8.2**. Readiness fails at heap 91–93%. Avery 502 is **connection closed during replica recycle**, then DB replay lookup **ok** on `idempotency_record`. Table is still the source of truth; the map is a growing copy. Next: histogram — are retained bytes in cache entries / `ConcurrentHashMap` nodes / replay payloads, not random `char[]` with no owner?

Gate 3: Histogram names the retainer. After a full GC, old gen still **1280 MB**. **`IdempotencyRecord` × 1,102,884 (~176 MB)** matches cache `size=1102880`. **`ConcurrentHashMap$Node` × 1,102,890**. `[C]` / `[B]` sit on top (payloads of those records). `Payment` / `Account` are **thousands**, not millions. Priya: east-1 `IdempotencyRecord` **1,104** (DB-backed, no map). Mechanism: 3.8.2 in-process replay cache, **maxSize=-1 ttl=0**, copies every miss into a CHM. Not a GC bug. Bounce is not a close-out.

## Supporting evidence

| File | Quote |
|---|---|
| timeline 23:10 06 Oct | Jordan: **3.8.2** on east-2; east-1 stays 3.8.0 |
| timeline 20:15 07 Oct | Priya: east-2 old gen **780 MB** vs east-1 **240 MB** |
| dashboard | east-2 old gen 212 → **1288 MB**; **does not return** after collect; east-1 ~220 MB flat |
| dashboard | Recycle 12:04 / 13:51: heap ~520 then climbs again |
| dashboard | Avery `c802d222-…` **502** on recycle, **201** on east-1 same key |
| logs 23:10 | `IdempotencyReplayCache enabled=true maxSize=-1 ttlSeconds=0` |
| logs 21:42 | cache size=**1102880** estimatedBytes=**612441088** |
| logs 21:44 | `idempotency_record` lookup **ok** after recycle |
| heap-histogram | `IdempotencyRecord` 1,102,884; CHM Node 1,102,890; Payment only 2,204 |

No thread dump in this pack (not a hang). `jcmd <pid> GC.class_histogram` is the live equivalent of this teaching file.

## Next investigation

Heap histogram on **east-2**: which classes dominate **instances and retained bytes**? Looking for `IdempotencyReplayCache` / map nodes / replay DTOs vs only `byte[]`/`char[]` with no owner. A **second histogram an hour later** would confirm growth of those classes (one snapshot is not a leak). Thread dump omitted — not a hang. No need to invent GC death-spiral numbers; dashboard already says old gen does not return.

## Stabilization action

**Drain `pay-prod-east-2`** from the LB (502s are recycle/readiness, not east-1). Keep **3.8.0**. If the cache flag can flip without a heap already at 91%, disable `idempotency-replay-cache` on east-2; otherwise leave it out of rotation. A bounce **buys hours** (heap returns to ~520) and **does not remove** the unbounded map.

Do **not**: raise `-Xmx` as the fix; bounce Postgres; bounce `dmgr-east`; treat recycle as close-out; roll 3.8.2 to east-1.

## Remediation

- Cache **maxSize + TTL**, or remove the in-process map. `maxSize=-1 ttl=0` is the defect.
- **Source of truth after restart** is `idempotency_record` (already 2.1M, shared). `Idempotency-Key` must still replay from the **table**. A cache may lose entries.
- Cap relative to a day’s unique Harbor Market keys — not “keep every key forever.”
- “Just give the JVM 8g” only delays the same climb.
- Second histogram after a hold: `IdempotencyRecord` count must stop tracking uptime.

## Communication update

SEV-2 is the **3.8.2 canary only**. `pay-prod-east-1` is flat and already returned 201 for Avery `c802d222-…` (same Idempotency-Key). East-2 old generation has climbed for two days and does not drop after GC; two recycles only reset the chart. We are taking east-2 out of the load balancer and **not** raising heap or touching the database. Next update when the canary is drained and create 502s stop.
