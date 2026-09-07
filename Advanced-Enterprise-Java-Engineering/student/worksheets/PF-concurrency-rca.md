# Portfolio artifact — Concurrency RCA

**Course:** Advanced Enterprise Java Engineering  
**Module:** 2 — Advanced Java Concurrency  
**Artifact id:** PF-02  
**Sources:** BREAKFIX-201 / INC-JVM-201 and INCIDENT-202 / INC-JVM-202  
**Case study:** BayPay Financial Services (fictional)

Export this file (or a copy) when you submit. Do not paste instructor solution text. All names and ids you cite must come from the synthetic packs.

**Student:**  
**Date:** 2026-09-06

---

## 1. BREAKFIX-201 — Duplicate payment

### Symptom

Unsafe starter under parallel load did not hold the two invariants. Case A (unique keys) landed around **75000** cents / **954** journal rows versus expected **100000** / **1000**. Case B (retries of `harbor-8841`) can post more than once when check-then-act loses. Merchant sees a retry storm become extra debits.

### Hypothesis timeline

| Time | Hypothesis | Evidence that supported or killed it |
|---|---|---|
| After first Case A | Lost updates on `balances.get` then `put` | Total below 100000 while some keys posted |
| After reading starter | `contains` then `add` on `seenKeys` is check-then-act | Two threads can both see “new key” |
| After `SafePaymentLedger` | `putIfAbsent` then `merge` holds both cases | Three green harness runs: A `100000`/`1000`, B `8400`/`1` |

### Root cause (your words)

Two compound actions were not atomic: (1) “have I seen this idempotency key?” as contains-then-insert, (2) “add cents to the account” as get-then-put. `ConcurrentHashMap` does not make those two-step stories safe. `CopyOnWriteArrayList` for the journal is fine only after the key is claimed.

### Repair

`putIfAbsent` on the key; if the key already existed, return false and add no money. If the insert won, `merge` the cents and append the journal row. Validated Case A and Case B with the JUnit harness (8 threads). Production still needs a unique `idempotency_key`.

### Stabilize vs remediate

| Stabilize | Remediate |
|---|---|
| Stop the retry storm / pause the racy canary; replay from a journal you trust | Atomic claim-then-add in process; unique DB key + one transaction in production |

### Production follow-up

`IdempotencyService.findReplay` plus a unique constraint on the key is the system of record. A second JVM with a heap map will still double-post. Harbor Bike retries become **200** with the original `paymentId`, not a second ledger row.

---

## 2. INCIDENT-202 — Workers not completing

### Symptom

Dashboard `pay-canary-weekday` on `sale-canary-1` pid 4412, 15:04–15:20 UTC: payment completed rps **0.0–0.4**, refund completed rps **0.0**, posting queue **180 → 640**, in-flight HTTP > 30s **22–28**, CPU **3–5%**, heap ~501 MB / 1 GB, GC quiet, JDBC 0, outbound HTTP 0, `/actuator/health` and liveness **UP**. HTTP accept rps stayed 28–35; 5xx stayed ~0.3% because calls did not finish.

### Hypothesis v1 (before the dump)

Written after timeline + dashboard + logs. Classic lock-order deadlock on Avery’s active account. Logs at `15:04:12.443Z`: `payment-worker-3` `LOCK_ACQUIRED accountLock`, `refund-worker-1` `LOCK_ACQUIRED ledgerLock`. Then payment `LOCK_WAIT ledgerLock`, refund `LOCK_WAIT accountLock`. Last commits were `15:03:41` / `15:03:58`. Would be killed by a dump with no circle, or wait on JDBC/queue.

### Hypothesis v2 (after the dump)

Dump `2026-08-21 15:13:07` confirms AB-BA:

- `payment-worker-3` `BLOCKED` at `InMemoryLockManager.lockLedger:48`, waiting to lock `<0xf0ae1110>`, already locked `<0xf0acc001>`, from `PaymentWorker.postAuthorized:77`.
- `refund-worker-1` `BLOCKED` at `InMemoryLockManager.lockAccount:33`, waiting to lock `<0xf0acc001>`, already locked `<0xf0ae1110>`, from `RefundWorker.reverse:64`.
- JVM: `Found 1 deadlock.` payment-worker-3 waits for monitor held by refund-worker-1 and the reverse.
- `payment-worker-0..2` BLOCKED on `lockAccount` / `0xf0acc001`. `refund-worker-0,2,3` BLOCKED on `lockLedger` / `0xf0ae1110`.
- HTTP exec-11 / exec-18 `WAITING` on `CompletableFuture.join` in `PaymentController.create` / `RefundController.create`. exec-2 `RUNNABLE` in health — that is why actuator stayed UP.

### Root cause (your words)

Payment and refund take the same two heap monitors in opposite order. One Harbor Bike payment (`pay-harbor-new`) and one refund (`ref-harbor-8841`) closed the circle. Every other worker queued behind those monitors. Completions dropped, queue climbed, CPU went idle. Health does not take the posting locks.

### Stabilize vs remediate

| Stabilize | Remediate |
|---|---|
| Drain canary from the LB, bounce pid 4412 (optionally pause refunds first) | One lock order (or one money lock / map-only verbs); lock timeouts; readiness fails on queue depth / stuck in-flight |

### Lock or concurrency policy you would enforce

Every money path takes locks in one written order (account, then ledger) or uses a single exclusive money lock — payment and refund never invert that order.

---

## 3. Communication samples

### Internal bridge (INC-JVM-201 or 202 — pick one)

What we know / do not know / next update:

**INC-JVM-202.** We know completions on `sale-canary-1` fell at 15:04, health is UP, CPU is idle, queue is climbing, and the 15:13 dump shows `payment-worker-3` and `refund-worker-1` waiting on each other’s monitors (`0xf0acc001` / `0xf0ae1110`). We do not know whether Harbor Bike already retried with a new key or whether other canaries ship the same lock order. Next update in 15 minutes after we drain and bounce this instance.

### Merchant-safe note

Harbor Bike invoice-8841 and a new checkout are still in progress on our side. We have taken that canary out of traffic and are restoring posting. We will confirm whether those two requests completed or need a safe retry with the **same** idempotency key. We are not stating a customer-facing “deadlock” or a dollar amount we have not reconciled.

---

## 4. ARCHITECT-203 — prevention paragraph

How your design would have prevented both incidents (5–8 sentences). Link to `labs/ARCHITECT-203/work/DESIGN.md` if you wrote one:

BREAKFIX-201 is a lost update: claim the key with `putIfAbsent`, then `merge` the cents. INCIDENT-202 is opposite lock order on `accountLock` and `ledgerLock`. ARCHITECT-203 uses no second monitor — per-key map verbs plus a bounded platform pool — so payment and refund cannot wait on each other. A refund is the same claim-then-merge path (negative cents) with one admission semaphore. The heap is not the control once a second JVM exists; the unique `idempotency_key` is. The slice still has a crash window between `putIfAbsent` and `merge`; production closes that with one database transaction. Design note: `labs/ARCHITECT-203/work/DESIGN.md`.

---

## 5. Interview talking points

Write four bullets you would actually say, labeled Engineer / Senior / Staff / Principal:

- Engineer: I dump threads when completions die and CPU is idle. I quote the waiting thread and the monitor, I do not guess GC.
- Senior: Check-then-act on a `ConcurrentHashMap` is still a race. `putIfAbsent` then `merge`. Unique key in the database is what survives a second instance.
- Staff: Stabilize is drain-and-bounce. Remediate is one lock order and a readiness probe that sees the posting queue, not `/liveness`.
- Principal: The modular monolith can post in-process; two JVM workers need an outbox and a unique index, not a smarter heap lock.

---

## Honesty

- [x] I did not open `solutions/` before attempting both labs
- [x] I requested INC-JVM-201 and INC-JVM-202 evidence in the documented order
- [x] Every numeric claim has a source (harness, dashboard, or log line)
