# Instructor solution — ARCHITECT-203

Students may see a short version in the lab’s details block after they attempt. This file is the full instructor key.

## Design

Single-JVM canary that would have survived BREAKFIX-201 and INCIDENT-202, with an honest multi-instance story.

### Collections

| Concern | Type | Verb |
|---|---|---|
| Idempotency | `ConcurrentHashMap<String, String>` | `putIfAbsent(key, paymentId)` |
| Account totals | `ConcurrentHashMap<String, Long>` | `merge(accountId, amount, Long::sum)` |
| Journal | `ConcurrentLinkedQueue<Entry>` | `offer` / iterate |
| Metrics | `LongAdder` | `increment` outside the money path |

Do not use `ArrayList` as a shared journal. Do not use `get` + `put` for keys or totals.

### Compound update

```text
if (putIfAbsent failed) return false;  // replay
merge(account, amount);
offer(journal entry);
return true;
```

Crash window remains between the three calls. State that in `DESIGN.md`. Production: one `@Transactional` method + unique `idempotency_key` (`IdempotencyService`).

Refunds: `merge(account, -amount)` only after a successful `putIfAbsent` on a refund key, or take the **one-lock** path below so journal and total stay paired.

### Threads and admission

For this CPU-light slice, `newFixedThreadPool(8)` plus the harness is enough. If the design includes blocking HTTP authorize, `newVirtualThreadPerTaskExecutor()` plus a `Semaphore` (e.g. 500) matching the downstream quota.

- Queue: bounded (`ArrayBlockingQueue`) if using a platform `ThreadPoolExecutor`.
- Reject: `AbortPolicy` → fail the request. Never `DiscardPolicy`.
- Shutdown: `shutdown` + `awaitTermination` in `close()`.

Do not hold `synchronized` across a network call (pinning + latency).

### Lock policy (one sentence)

**“Money movements use ConcurrentHashMap atomic verbs only; if a second exclusive section is ever required, both payment and refund take a single private moneyLock and no other lock.”**

That sentence prevents INCIDENT-202. If a team insists on two locks, the sentence becomes: **“Always accountLock then ledgerLock; never the reverse.”** Prefer one lock.

### Multi-instance

Heap maps do not exclude a second pod. The system of record is the unique idempotency row and a transactional ledger insert. The canary is a single-instance accelerator and a teaching harness.

### What we will not solve

Kill -9 mid-method, cross-region active-active, exactly-once with a broker (needs an outbox — later modules).

## Small code (reference shape)

```java
public boolean authorize(String paymentId, String key, String accountId, long amountCents) {
    if (seen.putIfAbsent(key, paymentId) != null) {
        return false;
    }
    balances.merge(accountId, amountCents, Long::sum);
    journal.offer(new Entry(paymentId, key, accountId, amountCents));
    accepted.increment();
    return true;
}
```

A student who instead uses one `synchronized (moneyLock)` around an ordinary `HashMap` + `ArrayList` can still meet the harness and should lose some Trade-off / Production points if they claim that is the long-term architecture.

## How this prevents the two incidents

- BREAKFIX-201: `putIfAbsent` + `merge` + concurrent journal removes the three races.
- INCIDENT-202: one lock or zero multi-lock removes circular wait.

## Scoring note

A design that only says “use virtual threads and ConcurrentHashMap” without verbs, bounds, and a lock sentence is incomplete. The details block in the student lab is a hint after attempt, not a license to skip `DESIGN.md`.
