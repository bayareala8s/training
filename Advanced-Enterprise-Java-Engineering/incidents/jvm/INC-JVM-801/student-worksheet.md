# INC-JVM-801 student worksheet

Fill in order. Quote evidence. Do not paste instructor solutions.

**Incident:** Canary CPU 98 percent  
**Instance:** `pay-prod-east-2` (canary) vs `pay-prod-east-1`  
**Your name / cohort:**  
**Time started:** 2026-09-06  
**Time submitted:** 2026-09-06

## Current hypothesis

(What do you think is happening? Update after each gate.)

Gate 1: SEV-2 is **`pay-prod-east-2` only** (canary **3.8.1** since 09:40). Process CPU **98%**, p99 **9.4s**, 74 in-flight, Tomcat 81/200. **`pay-prod-east-1` (3.8.0)** CPU 12%, p99 ~180 ms, Avery retry **201**. Heap 540/1536, old gen flat, GC p99 **19 ms** — not a pause/leak page. Hikari 11/50 pending **0**, DB CPU 17% — not INC-402. Liveness UP, readiness flickering (HTTP slow). 98% CPU is a **symptom**: the HTTP threads are **busy**, not waiting on the pool. First guess: 3.8.1 put expensive work on the create-payment path. Next: logs (who, how long), then a dump — **what frames are RUNNABLE?** Do not roll 3.8.1 to east-1. Do not bounce Postgres or `dmgr-east`.

Gate 2: Logs name a **3.8.1 feature**, not a closed RCA. Avery `c801d111-…` accepted then “still in flight 9661 ms”; `RequestBodyPiiScanner` **body scan finished elapsedMs=9412 contentLength=184422**; then 201 in 10392 ms. Other scans 3881 ms / 96 KiB, 7210 ms / 156 KiB. One create **timed out after 10000ms**. Feature `request-body-pii-scan enabled=true` on east-2 3.8.1. Scan time tracks body size and sits **on the HTTP create path** — that matches busy Tomcat + high CPU + some 201s. Still need stacks: is the thread **RUNNABLE** in the scanner (CPU), or blocked on I/O? Next: dump — quote frames, not just RUNNABLE.

Gate 3: Dump answers the written question. Six `http-nio-8080-exec-*` threads are **RUNNABLE** in `java.util.regex.Pattern$Curly.match0` → `String.matches` → `RequestBodyPiiScanner.scan:88` → `doFilter:41`. CPU times 8–18 s on those threads. RUNNABLE + regex + filter on the HTTP chain is the **hot method story**, not “CPU is high.” One exec is in `HealthIndicator` (readiness flicker). One TIMED_WAITING on Hikari `isValid` is incidental (pending 0). Mechanism: 3.8.1 enabled **request-body-pii-scan** on the Tomcat thread; catastrophic-looking regex (`Curly.match0`) on 96–184 KiB bodies burns a core per in-flight POST.

## Supporting evidence

| File | Quote |
|---|---|
| timeline 16:40 | Jordan: 3.8.1 on **east-2** only; east-1 stays 3.8.0. Riley: do not roll 3.8.1 to east-1 |
| dashboard 10:24 | east-2 CPU **98%**, p99 **9.4s**, 74 in-flight; east-1 CPU 12%, p99 180 ms |
| dashboard | Heap 540/1536, GC p99 19 ms; Hikari 11/50 pending 0; DB CPU 17% |
| dashboard notes | LB still ~15% to east-2; Avery `c801d111-…` hung on east-2, **201 on east-1** |
| logs 17:18 | `RequestBodyPiiScanner` elapsedMs=**9412** contentLength=**184422**; then 201 in 10392 ms (`a8010001-…`) |
| logs 17:20 | `Request timed out after 10000ms` (`a8010003-…`) |
| logs 17:23 | `request-body-pii-scan enabled=true` instance=east-2 version=3.8.1 |
| thread-dump exec-14 | RUNNABLE `Pattern$Curly.match0` → `RequestBodyPiiScanner.scan:88` cpu=18440 ms |
| thread-dump exec-19/7/22/3/31 | same scanner/regex; exec-8 TIMED_WAITING Hikari (not the page) |

No heap histogram in this pack (not needed). Local confirm: `jcmd <pid> Thread.print` on `reference-apps/baypay` would show the same state words; this page is synthetic.

## Next investigation

Thread dump on **east-2**: are the busy HTTP threads **RUNNABLE** inside `RequestBodyPiiScanner` (or a regex / JSON walk), or WAITING/BLOCKED on Hikari/DB? A single dump cannot prove a hot method — a second dump one minute later would confirm the same frames. Heap histogram omitted; I do not need it (heap/GC already quiet). No container metrics needed (CPU is process, not a cgroup kill).

## Stabilization action

**Drain / remove `pay-prod-east-2` from the load balancer** (it still takes ~15%). Keep **east-1** serving; Avery’s retry already 201 there (same Idempotency-Key). Disable the 3.8.1 feature flag on east-2 *if* that is a hot config flip without a restart; otherwise leave the process up but out of rotation (liveness is not the product).

Do **not**: roll 3.8.1 to east-1; bounce Postgres; bounce `dmgr-east` / `Pay2`; region failover; add replicas (only the canary is hot); raise Tomcat to 2000.

## Remediation

- Turn **request-body-pii-scan** off by default, or run it on a **bounded sidecar / queue** with a **body-size cap** — not on the HTTP thread that also talks to the ledger.
- Replace `String.matches` / unbounded `Curly` regex on the full body. Size-cap relative to a legitimate Harbor Market checkout (184 KiB is already a scan tax, not a checkout).
- Canary gate: p99 and process CPU vs east-1 **before** raising weight. 3.8.1 vs 3.8.0 split is what made this visible.
- Second dump one minute later would have confirmed the same frames; keep that in the runbook.

## Communication update

SEV-2 is the **3.8.1 canary only**. `pay-prod-east-1` (3.8.0) is completing Harbor Market / Avery creates (retry of `c801d111-…` already 201). East-2 is at 98% CPU with p99 ~9s; database and the connection pool are not exhausted. We are taking east-2 out of the load balancer and **not** rolling 3.8.1 to east-1. Next update when east-2 is drained and create p99 on the remaining replica is back under SLO.
