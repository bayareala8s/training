# ARCHITECT-203 — In-process authorize worker

BayPay canary, one JVM. Demo account `22222222-2222-2222-2222-222222222221`.
Response to BREAKFIX-201 (lost update) and INCIDENT-202 (AB-BA locks).

## Picture

```text
harness / HTTP
    → Semaphore(32)   reject money work; never DiscardPolicy
    → fixed platform pool (8)
    → ConcurrentHashMap.putIfAbsent(idempotencyKey)
          miss → return false, no money
          insert → ConcurrentHashMap.merge(account, cents)
                 → ConcurrentLinkedQueue.offer(journal row)
    → LongAdder accepted / rejected   (outside the money story)
refund path enters the same claim-then-merge (negative cents, own key)
```

No `accountLock` then `ledgerLock`. Payment and refund cannot invert two monitors.

## Collections and verbs

| Structure | Verb | Why |
|---|---|---|
| `ConcurrentHashMap<String, Boolean> keys` | `putIfAbsent` | At most one winner per idempotency key |
| `ConcurrentHashMap<String, Long> balances` | `merge` | Lost-update safe add |
| `ConcurrentLinkedQueue<Entry> journal` | `offer` | No shared `ArrayList` without exclusion |
| `LongAdder` | `increment` | Metrics; not inside a money lock |

Order is always: claim key → merge cents → offer journal. If `putIfAbsent` loses, stop.

## Threads and admission

This slice is CPU-light (map ops). A **fixed platform pool of 8** is enough and easy to `jstack`. Virtual threads would be the later choice if authorize blocked on HTTP; they do not replace idempotency.

Bound: `Semaphore(32)` around `authorize` / `refund`. Exhausted → return false (reject). Do not `newCachedThreadPool` for a sale. Do not `DiscardPolicy` — that drops money work with no client error.

Rejection is “not accepted,” not “accepted and forgotten.”

## Lock policy (one sentence)

No explicit multi-lock: every money movement claims its idempotency key with `putIfAbsent` and then `merge`s the account total; payment and refund never take two monitors.

Refund uses the same sentence. It does not acquire a second lock “for the ledger.”

## Multi-instance

This heap map is a canary teaching aid. The day a second JVM exists, `IdempotencyService` plus a unique index on `idempotency_key` is the system of record. Two processes both winning `putIfAbsent` locally will double-post. Do not “fix” that with a longer heap lock.

## What this slice will not do

- Exactly-once after kill -9 between `putIfAbsent` and `merge` (key claimed, cents missing) or between `merge` and `offer` (total ahead of journal).
- Cross-JVM exclusion.
- Durable audit or crash recovery.
- JDBC / outbound I/O inside any lock (there is no lock to hold across I/O).

Production closes the crash window with **one database transaction** that inserts the idempotency row, the payment, and the ledger line.

## Why this would have stopped the two incidents

BREAKFIX-201 raced on contains-then-add and get-then-put. `putIfAbsent` + `merge` is the compound story. INCIDENT-202 deadlocked because payment locked account then ledger and refund locked ledger then account. This design has no second monitor, so that circle cannot form. A retry of `harbor-8841` is one journal row.

## Readiness (ops)

Liveness = process alive. Readiness should fail when the admission semaphore is exhausted or authorize p99 / queue age exceeds a budget. INCIDENT-202 stayed `UP` while workers were `BLOCKED`.
