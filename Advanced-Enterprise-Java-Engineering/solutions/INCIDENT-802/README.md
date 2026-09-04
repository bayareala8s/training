# INCIDENT-802 — Instructor solution

**Do not share this file with students before they submit a worksheet.**

## RCA

Canary `payment-service` **3.8.2** added `IdempotencyReplayCache` as a `ConcurrentHashMap` with **no TTL and no eviction**. Every unique create key retains an `IdempotencyRecord` plus `char[]` / `byte[]` for keys and payloads. Old generation climbs for two days (212 MB → 1288 MB) and **does not return** after full collections. Histogram is dominated by `IdempotencyRecord`, `[C`, `[B`, and `ConcurrentHashMap$Node`. Instance count matches the cache `size=` log.

This is **not** a GC bug. Allocation rate is ordinary. `pay-prod-east-1` on 3.8.0 stays flat. The database `idempotency_record` table remains the source of truth and is shared; the in-process map is a growing duplicate.

Distinct from INCIDENT-805: that page is short-lived `String`/`char[]` at huge allocation rate, not a retained old-gen set.

## Stabilization

1. Bounce the canary **and** disable the in-process cache (flag / revert 3.8.2 / set max size 0) so the climb does not restart.
2. Optionally drain `pay-prod-east-2` until the flag is off.
3. Do **not** bounce Postgres.
4. Do not bounce `dmgr-east`.
5. Do not treat “raise `-Xmx`” as the fix — it only delays the next recycle.

## Remediation

- Replace the unbounded map with **Caffeine** (or equivalent) **size + TTL**.
- The cache is **not** the source of truth. The DB idempotency table still is; a restart must remain correct.
- Bound estimated bytes; alert on cache size and old-gen retained after full GC.
- Canary gate: old-gen slope over 6–12 hours, not only first-hour p99.
- Test: N unique keys must not retain N records forever.

## Evidence students should have used

| Gate | What it shows |
|---|---|
| Dashboard | east-2 old gen climb across two days; east-1 flat; full GC does not reclaim; allocation rate modest |
| Logs | 3.8.2; cache `maxSize=unbounded ttl=none`; size/bytes grow in lockstep; DB replay still works |
| Histogram | `IdempotencyRecord` ~1.1M; `[C]`/`[B]` dominate bytes; counts match cache size |

A worksheet that says only “leak” with no class names and no growth interval scores poorly on Diagnostic method even if the word is right.

## Comms (acceptable example)

SEV-2 on `pay-prod-east-2` after 3.8.2. Old generation has climbed for two days and is not returning after collections. `pay-prod-east-1` is healthy. We are taking the canary out (or bouncing it after disabling the new in-process cache). Idempotency for retries still depends on the shared table. Next update 20 minutes.
