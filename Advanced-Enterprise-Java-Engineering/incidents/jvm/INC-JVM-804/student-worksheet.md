# INC-JVM-804 student worksheet

Fill in order. Quote evidence. Do not paste instructor solutions.

**Incident:** HTTP workers exhausted on canary  
**Instance:** `pay-prod-east-2` (canary) vs `pay-prod-east-1`  
**Your name / cohort:**  
**Time started:** 2026-09-06  
**Time submitted:** 2026-09-06

## Current hypothesis

(What do you think is happening? Update after each gate.)

Gate 1: SEV-2 is **`pay-prod-east-2` (3.8.2)** only. Tomcat **200/200**, accept queue **96**, p99 **12s**. Hikari **8/50** pending 0, DB CPU **15%** — **not** INC-402. `fx-east` `/quote`: east-1 38 ms; east-2 **no success samples**, 8 in-flight; jump-host GET **>30s**. east-1 **`fx-quote-on-create` off**, Avery (USD) retry **201**. Liveness UP; readiness fails (`no free worker`). First guess: HTTP workers are **parked on FX**, not making progress. 200/200 is a **symptom**. Do not raise Tomcat max (those extras would wait on the same call). Next: logs (timeouts, waiters), then dump — **WAITING on which client?**

Gate 2: Logs name the **outbound client**, not “pool too small.” Feature `fx-quote-on-create` **poolSize=8 connectTimeout=none readTimeout=none**. Quotes **inUse=8 queued=71**, still in flight **188s**. Avery is **USD** and still `quote submitted`. Create **awaits fx quote before persist**. Inbound **timed out after 12000ms**; outbound timeout=**none**. Hikari `active=8 idle=42 waiting=0`. HTTP 200/200 is workers parked behind an 8-wide FX pool with **no timeout**. Next: dump — `WAITING` on `FxQuoteClient` / HTTP client / `poolWaiters`, not `BLOCKED` on money locks (803) and not `RUNNABLE` regex (801).

Gate 3: Dump names the waiter. HTTP execs are **WAITING (parking)**: `CompletableFuture.join` → `FxQuoteClient.quote:74` → `create:79` (workers that got a slot), or `LinkedBlockingQueue.take` → `FxQuoteClient.acquire:41` (waiters for the 8-wide pool). **`fx-client-1/2` RUNNABLE** in `NioSocketImpl.park` / `HttpClientImpl.send` / `doGet:99` — outbound read with **no timeout**. Health thread RUNNABLE — liveness UP. Not BLOCKED on money locks, not Hikari. Tomcat 200/200 is inbound workers **joined to 8 hung sockets**.

## Supporting evidence

| File | Quote |
|---|---|
| timeline 17:40 | Jordan: `fx-quote-on-create` on east-2 3.8.2 |
| timeline 18:02 | Priya: `fx-east` p99 → **no samples** (probe timeouts) |
| dashboard | Tomcat **200/200**, accept queue 96; Hikari **8/50** pending 0; DB CPU 15% |
| dashboard | `fx-east` east-2 **no success samples**, 8 in-flight; jump-host GET **>30s** |
| dashboard | east-1 feature **off**; Avery USD retry **201** |
| logs 17:40 | `poolSize=8 connectTimeout=none readTimeout=none` |
| logs 18:06 | quote in flight **188400 ms** inUse=8 queued=71 |
| logs 18:10 | `create path awaiting fx quote before persist` |
| dump exec-4 | WAITING `CompletableFuture.join` `FxQuoteClient.quote:74` |
| dump exec-91 | WAITING `acquire:41` `LinkedBlockingQueue.take` |
| dump fx-client-1 | RUNNABLE `NioSocketImpl.park` `doGet:99` |

No histogram in this pack.

## Next investigation

Thread dump on **east-2**: what are the 200 `http-nio-8080-exec-*` threads waiting on? Expect `WAITING`/`TIMED_WAITING` in `FxQuoteClient` or the HTTP client, plus waiters on the **8-slot** pool. Heap omitted (not a leak). Hikari gauges already contradict a JDBC waiter.

## Stabilization action

**Drain `pay-prod-east-2`** (east-1 already 201’d Avery). **Disable `fx-quote-on-create`** on that canary (hot flag if it exists). For a **USD** Harbor Market checkout, **fail-open / skip quote** is acceptable stabilize — FX is a preview field, not the ledger. Do not wait for `fx-east` to recover while 200 workers stay parked.

Do **not**: `server.tomcat.threads.max=2000` (those threads wait on the same 8 sockets); bounce Postgres; bounce `dmgr-east`; treat Hikari as the page.

## Remediation

- **Outbound timeouts** (`connect` + `read`) shorter than inbound 12s. Inbound timeout without outbound timeout is this incident.
- **Bulkhead:** pool of 8 is the intended quote concurrency — HTTP must not `join`/`take` unbounded. Reject or skip when `inUse==8`.
- **Circuit breaker** on `fx-east` after probe timeouts (Priya already had the signal).
- FX **off the create path** for USD (cache / async). Avery’s account is USD.
- Fail-open vs fail-closed: USD Harbor Market can **fail-open** (skip preview). Multi-currency that *requires* a rate should fail-closed **after** a short timeout, not hang the servlet pool.

## Communication update

SEV-2 is the **3.8.2 canary only**. Tomcat is 200/200 there; the database and Hikari are idle. `pay-prod-east-1` is completing Harbor Market / Avery (`c804d444-…` 201 on retry). Creates on east-2 are waiting on `fx-east` quotes with no client timeout. We are draining east-2 and leaving FX-on-create **off**. We are not raising Tomcat max. Next update when accept-queue is zero and create p99 on the remaining replica is back under SLO.
