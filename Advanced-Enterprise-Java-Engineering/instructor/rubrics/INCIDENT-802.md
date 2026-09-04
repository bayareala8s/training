# Rubric — INCIDENT-802

**Type:** INCIDENT  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

A lucky “it’s a leak” with no growth story and no histogram classes must **not** max Diagnostic method (20%).

| Dimension | 5 | 3 | 1 |
|---|---|---|---|
| Technical accuracy | 3.8.2 `IdempotencyReplayCache` unbounded `ConcurrentHashMap`; old gen retained; histogram `IdempotencyRecord`/`[C]`/`[B]`; not a GC bug | Leak named; cache or old gen mentioned; mechanism fuzzy | “Tune G1” or “Postgres is leaking” as RCA |
| Diagnostic method | Gate 1→2→3; histogram opened to answer a written question; classes quoted | Used all files; skipped a hypothesis | Opened solutions or the histogram first |
| Production awareness | Bounce canary **and** disable/cap cache; no Postgres bounce; `-Xmx` not the fix | Bounce only | Bounce the database or leave the map enabled |
| Trade-off analysis | Caffeine/size+TTL vs unbounded map; cache is not source of truth | Mentions TTL | “8g heap” as strategy |
| Security / reliability | Idempotency still correct after eviction because the table remains; duplicate-charge risk if cache were the only store | Mentions retries | Drops idempotency to save memory |
| Communication | Replica-scoped; does not announce a leak before quoting growth + classes | Usable, slightly over-confident | Blames “the leak” in the first sentence with no evidence |
| Efficiency | 45–75 minutes | Complete but slow | Incomplete worksheet |

Stabilization that only says “restart the JVM” without disabling or bounding the cache loses Production awareness.
