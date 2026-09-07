# INC-JVM-803 student worksheet

Fill in order. Quote evidence. Do not paste instructor solutions.

**Incident:** Payment creates hang after nightly window  
**Instance:** `pay-prod-east-2` (canary) vs `pay-prod-east-1`  
**Your name / cohort:**  
**Time started:** 2026-09-06  
**Time submitted:** 2026-09-06

## Current hypothesis

(What do you think is happening? Update after each gate.)

Gate 1: SEV-2 is **`pay-prod-east-2` only** after `NightlyReversalJob` started (02:00, same JVM). Completions **0**, in-flight **61**, CPU **4%**, sampled **BLOCKED 22**. Heap/GC quiet (not 801/802). Hikari **3/50** pending 0, DB CPU 16% (not INC-402). east-1 **3.8.0**, job **off**, Avery retry **201**. Liveness/readiness UP — probes do not take app monitors. First guess: HTTP creates and the nightly job are **stuck on Java monitors**, not the database. “Deadlock” is a title, not an RCA until we quote owners. Next: logs (job vs create), then dump — **who owns which monitor?** Do not enable the job on east-1. Do not bounce Postgres or `dmgr-east`.

Gate 2: Logs show a **lock-order clash**, not a closed dump. Job `LOCK_ACQUIRED ledgerLock` on `nightly-reversal-1`. Avery create `LOCK_ACQUIRED accountLock` on `http-nio-8080-exec-16` (`PaymentApplicationService.create`), then `LOCK_WAIT ledgerLock ownerHeldBy=nightly-reversal-1`. Job then `LOCK_WAIT accountLock ownerHeldBy=http-nio-8080-exec-16`. Later creates wait on `accountLock` behind exec-16. Job still `waiting` (12/118). Word “deadlock” is not in the log — do not close on it. Next: dump — **BLOCKED vs monitors**; quote `<owner>` / waiting to lock. Not INC-202 (`payment-worker` vs `refund-worker`).

Gate 3: Dump quotes the circular wait. **`nightly-reversal-1` BLOCKED** `lockAccount:41` waiting `<0xf0acc801>` (account), **owns `<0xf0ae1880>`** (ledger) from `NightlyReversalJob.reverseOne:118`. **`http-nio-8080-exec-16` BLOCKED** `lockLedger:56` waiting `<0xf0ae1880>`, **owns `<0xf0acc801>`** from `PaymentApplicationService.create:88` (account taken at create:81). exec-21/9 wait on the same account monitor. JVM: **Found 1 deadlock** — heading is not the RCA; the two orders are. Hikari TIMED_WAITING on exec-4 is incidental. Health thread RUNNABLE — why probes stay UP. Not INC-202 (`payment-worker` / `refund-worker` are not in this dump).

## Supporting evidence

| File | Quote |
|---|---|
| timeline 23:55 | Jordan: `NightlyReversalJob` on **east-2 only**; east-1 does not run it |
| dashboard 02:15 | east-2 completions **0**, in-flight 61, CPU **4%**, BLOCKED **22**; Hikari 3/50 |
| dashboard | east-1 completions 4.2 rps; Avery retry **201** |
| logs 09:00 | job `LOCK_ACQUIRED ledgerLock` thread=`nightly-reversal-1` |
| logs 09:11 | exec-16 `LOCK_ACQUIRED accountLock` then `LOCK_WAIT ledgerLock ownerHeldBy=nightly-reversal-1` |
| logs 09:11 | job `LOCK_WAIT accountLock ownerHeldBy=http-nio-8080-exec-16` |
| dump nightly | waiting `<0xf0acc801>` locked `<0xf0ae1880>` `reverseOne:118` |
| dump exec-16 | waiting `<0xf0ae1880>` locked `<0xf0acc801>` `create:88` |
| dump footer | Found 1 deadlock: nightly ↔ exec-16 |

No histogram in this pack (heap quiet).

## Next investigation

Thread dump on **east-2**: which threads are `BLOCKED (on object monitor)`, which monitors they **own**, and which they **wait for**. Expect `nightly-reversal-1` vs `http-nio-8080-exec-16` and a waiter pile on `accountLock`. Heap histogram omitted (heap quiet). Not a Hikari story (pending 0). A “Found one Java-level deadlock” heading is not enough — quote threads and monitors.

## Stabilization action

**Drain `pay-prod-east-2`** so creates go to east-1 (already 201 for Avery). **Disable / do not start `NightlyReversalJob`** on that JVM. If the two threads stay BLOCKED, **bounce east-2 only** after drain — a bounce is stabilize (breaks the pair tonight), not remediation (same orders tomorrow at 02:00). Prefer killing the **job thread** if ops can interrupt it without bouncing HTTP; here they share a JVM, so drain-then-bounce is the safe card.

Do **not**: enable the job on east-1; bounce Postgres; bounce `dmgr-east`; add Tomcat threads; region failover.

## Remediation

- **One lock order:** account then ledger on **every** path (`create` already does that; `reverseOne` must match) — **or** drop nested in-process locks and use DB transactions only.
- Nightly reversal should **not** share the API JVM (INC-EE-402 / reporting-on-Pay1 smell).
- Bounce is not a close-out if 02:00 still exists with two orders.
- Contrast INC-202: that pack was `payment-worker` vs `refund-worker` on a teaching canary. This pack is `nightly-reversal-1` vs `http-nio-8080-exec-16` on `pay-prod-east-2`.

## Communication update

SEV-2 is **`pay-prod-east-2` only** after the 02:00 nightly job on that JVM. Completions there are zero; CPU is idle. `pay-prod-east-1` is still completing Harbor Market / Avery (`c803d333-…` 201 on retry). Database pool is not exhausted. We are draining east-2 and leaving the job **off** east-1. Next update when creates on the remaining replica stay at baseline and east-2 is out of rotation.
