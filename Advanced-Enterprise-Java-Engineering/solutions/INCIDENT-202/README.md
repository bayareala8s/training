# Instructor solution — INCIDENT-202

**Do not share this file with students before they attempt the lab.**

## Root cause

Lock-order inversion on two intrinsic locks in the canary worker.

| Thread | Holds | Waits for | Call site |
|---|---|---|---|
| `payment-worker-3` | `accountLock` (`0xf0acc001`) | `ledgerLock` (`0xf0ae1110`) | `PaymentWorker.postAuthorized` → `lockLedger` |
| `refund-worker-1` | `ledgerLock` (`0xf0ae1110`) | `accountLock` (`0xf0acc001`) | `RefundWorker.reverse` → `lockAccount` |

Payment path acquires **account then ledger**. Refund path acquires **ledger then account**. After 15:04:12 both hold one and wait for the other. Other payment workers queue on `accountLock`; other refund workers queue on `ledgerLock`. Completions drop to zero. CPU is idle. Health stays UP because actuator does not take those monitors. HTTP threads `join()` the worker futures and age out as `REQUEST_SLOW`.

This is a circular wait (Coffman). It is not a race on the totals, not GC, not JDBC, and not a dead process.

## Why the dump is sufficient

`thread-dump.txt` includes the JVM deadlock report and the two stacks. Logs already showed `LOCK_ACQUIRED` / `LOCK_WAIT` crossed at the same millisecond. The dashboard (both completion rates down, queue up, CPU down, JDBC 0) ruled out a hot loop and an external dependency.

Students who jump to “deadlock” from the lab title without quoting those stacks have not diagnosed.

## Remediation — pick one policy and enforce it

**Preferred for a canary: one lock.**

A single private `final Object moneyLock` (or one database transaction) for every capture and refund. Circular wait is impossible if there is only one monitor. Throughput is limited by that lock; for this in-memory canary that is acceptable.

**Alternative: one documented order.**

Every module acquires `accountLock` then `ledgerLock`, never the reverse. Refund code is rewritten to take account first. Add a review checklist and, if practical, an assertion or wrapper:

```java
void withAccountThenLedger(Runnable body) {
    synchronized (accountLock) {
        synchronized (ledgerLock) {
            body.run();
        }
    }
}
```

**Alternative: `tryLock` with timeout.**

Both paths use `ReentrantLock.tryLock` (e.g. 50 ms), release all locks on failure, and retry with jitter. Breaks hold-and-wait. Needs idempotent retry so a timeout cannot double-post (connects to BREAKFIX-201). Can livelock if both sides spin without backoff.

**Not a remediation:** bounce only. A bounce unsticks *this* circle and will recur on the next crossed payment/refund.

## Stabilization

1. Drain `sale-canary-1` from the load balancer so new HTTP does not `join()` forever.
2. Bounce the canary **after** the dump is captured (dump is already in the pack).
3. Pause refunds *or* payments if only one path can be stopped quickly — understand this does not fix the code.
4. Communicate: completions stopped; workers waiting on each other; we are taking the canary out; cause under analysis.

Do not tell merchants “database is down.” JDBC was 0.

## Evidence map (INC-JVM-202)

- Timeline: completions fall together at 15:04; health still UP.
- Dashboard: rps ≈ 0, queue climbing, CPU 3–5%, threads still alive.
- Logs: last commits 15:03:58; crossed `LOCK_ACQUIRED` / `LOCK_WAIT` at 15:04:12.443–.801.
- Dump: deadlock section; monitors match the log lock names.

## Common student misses

- “Restart the JVM” as the only close-out.
- Blaming `CompletableFuture.join` on the HTTP thread as the *cause* (it is a symptom amplifier).
- Adding a third lock.
- Reversing only one call site and leaving a third module that still uses the old order.

## Scoring note

Lucky guess of “lock order” without v1-before-dump and without quoted stacks must not max **Diagnostic method**. Technical accuracy can still be high if the policy is right.
