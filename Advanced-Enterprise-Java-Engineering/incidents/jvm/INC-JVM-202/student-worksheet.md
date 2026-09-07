# INC-JVM-202 student worksheet

Fill this as you request evidence. Hypothesis v1 **before** the thread dump.

**Incident:** INC-JVM-202  
**Student:**  
**Date:** 2026-09-06

## Hypothesis

### v1 (after timeline + dashboard + logs, before dump)

Time: 2026-09-06 (after logs, before opening `evidence/thread-dump.txt`)

What you think is happening:

Payment and refund workers deadlocked on two in-process monitors for the same Avery account. At `15:04:12.443Z` `payment-worker-3` acquired `accountLock` and then waited on `ledgerLock`; `refund-worker-1` acquired `ledgerLock` and then waited on `accountLock`. Completions for both paths fell together because later workers pile up behind those two locks. This is not GC, JDBC, outbound HTTP, or a dead process: dashboard CPU 3–5%, heap flat, JDBC 0, outbound HTTP 0, health UP, queue 180→640.

What would disprove it:

A dump where those two threads are `RUNNABLE` or parked on `LinkedBlockingQueue.take` / JDBC, or where only one monitor appears, or where `Found 1 deadlock` is absent and workers are just saturated on a slow call.

### v2 (after dump)

Time: 2026-09-06 after `2026-08-21 15:13:07` dump of pid 4412

Updated hypothesis:

Confirmed AB-BA deadlock in `InMemoryLockManager`. Payment takes account then ledger; refund takes ledger then account. Remaining payment workers wait on `accountLock` (`0xf0acc001`); remaining refund workers wait on `ledgerLock` (`0xf0ae1110`). HTTP threads are parked on `CompletableFuture.join` in the controllers, which is why accept rps stays up and 5xx stays low.

What the dump confirmed or killed:

Confirmed v1. Killed “starved of tasks”, “spinning”, “JDBC”, and “health means workers are fine.”

## Supporting evidence

| Claim | Source | Quote or metric |
|---|---|---|
| Completions drop together at 15:04:12 | timeline.json | `payment_completed_rps and refund_completed_rps fall together over ~90 seconds` |
| Process and health still look fine | dashboard.md | CPU **3–5%**, heap 501/1024 MB, GC p99 9 ms, `/actuator/health` UP, JDBC 0, outbound HTTP 0 |
| Queue and in-flight hang | dashboard.md | Posting queue **180 → 640**; in-flight HTTP > 30s **22–28**; HTTP 5xx still 0.3% |
| Last commits then lock wait | logs.txt | Last `POST_COMMIT`/`REFUND_COMMIT` at 15:03:41 / 15:03:58. At 15:04:12.443 payment owns `accountLock`, refund owns `ledgerLock`; 15:04:12.800 payment `LOCK_WAIT ledgerLock`; 15:04:12.801 refund `LOCK_WAIT accountLock` |
| Circle of two monitors | thread-dump.txt | `payment-worker-3` BLOCKED at `lockLedger` waiting `0xf0ae1110`, locked `0xf0acc001`. `refund-worker-1` BLOCKED at `lockAccount` waiting `0xf0acc001`, locked `0xf0ae1110`. JVM: `Found 1 deadlock.` |

## Next investigation

What you would request next if this were live:

`jstack` / thread dump of pid 4412 (this pack already has it). After stabilize: grep `InMemoryLockManager` for lock order on payment vs refund; confirm no second JVM shares these heap locks.

Expected finding:

Opposite lock order on the same two `Object` monitors; HTTP parked on worker futures.

## Stabilization

Action that restores completions now:

Drain the canary from the load balancer, then bounce pid 4412 (or pause refund admission first, then bounce). Do not keep sending Harbor Bike `/payments` and `/refunds` at a deadlocked JVM.

Risk (lost in-flight work, duplicate after bounce, etc.):

In-flight `pay-harbor-new` and `ref-harbor-8841` never `COMMIT`. Clients that retry without the same idempotency key can double-post after the bounce. Health stays UP until the instance is removed, so leaving it in the pool looks “healthy” while money is stuck.

## Remediation

Policy or code change you would require before the canary takes traffic again:

One lock order for every money path: account then ledger (or one private `moneyLock` / no multi-lock — map verbs only). Payment and refund must not take the two monitors in opposite orders. Time-bounded lock acquire; fail the work rather than wait forever. Readiness must fail when posting queue depth or in-flight age exceeds a threshold.

How you would test it:

Harness that runs a payment and a refund on the same account in a loop (INCIDENT-202 traffic shape) plus BREAKFIX-201 Case A/B. `jstack` under that load must not print `Found 1 deadlock`.

## Communication update

Audience: internal bridge (Riley / Jordan) plus a merchant-safe note for Harbor Bike support

What we know:

Since 15:04 UTC payment and refund completions on `sale-canary-1` dropped toward zero. The process is up, health is UP, CPU is idle, the posting queue is climbing. Harbor Bike invoice-8841 refund and a new checkout are stuck after AUTHORIZED. A thread dump at 15:13 shows two worker threads waiting on each other’s monitors.

What we do not know:

Whether any in-flight Harbor Bike amount committed after the dump. Whether other canaries share this lock code. Whether clients already retried with new keys.

Next update time:

15 minutes after bounce / drain decision (or 15:33 UTC if we hold the timeline clock).

## Self-check

- [x] Timeline → dashboard → logs → dump
- [x] v1 written before the dump
- [x] Dump quotes name threads and monitors
- [x] Stabilize and remediate are different
- [x] I did not open `solutions/INCIDENT-202` before attempting
