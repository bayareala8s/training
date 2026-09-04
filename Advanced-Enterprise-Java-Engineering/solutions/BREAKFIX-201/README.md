# Instructor solution — BREAKFIX-201

**Do not share this file with students before they attempt the lab.**

## Root cause

`UnsafePaymentLedger.authorize` performs three racy compound actions on shared state:

1. **Check-then-act on the idempotency map.** `seenKeys.get` then later `put` is two operations. Two workers both see “absent” for `harbor-8841` and both post `$84.00` (Case B, INC-JVM-201 `pay-7c21` / `pay-7c22`).
2. **Read-modify-write on the balance.** `getOrDefault` + `put` on a `ConcurrentHashMap` is not atomic. Distinct keys lose increments (Case A). Logs show two posts writing the same `balanceAfter` and the same `journalSeq`.
3. **Shared `ArrayList` journal.** `add` is not thread-safe. Rows disappear or the list throws under parallel append. A concurrent map for balances does not protect the list.

`ConcurrentHashMap` made each *single* `get`/`put` safe. It did not make the business method atomic. `volatile` would not have fixed the increment or the journal.

## Why tests missed it

A single-thread double call of the same key succeeds: the second `get` sees the first `put`. The sale produced parallel retries and parallel distinct keys. Visibility and atomicity bugs do not reliably appear on one core.

## Reference fix

See `SafePaymentLedger.java`:

- `putIfAbsent` for the key (first writer wins; others replay).
- `merge` for the account total.
- `ConcurrentLinkedQueue` for the journal.

The three calls are still not crash-atomic. A kill between `putIfAbsent` and `offer` can drop a row while the key stays marked. Production BayPay closes that window with one database transaction and a unique index on `idempotency_key` (`IdempotencyService` in `reference-apps/baypay`).

An equivalent exclusive fix is one private `final Object moneyLock` around get/put/add. That passes the harness and is easier to deadlock later if a second lock appears. Prefer the atomic map verbs for this canary; prefer the database for the real service.

## Stabilization vs remediation

| Stabilize (during the sale) | Remediate |
|---|---|
| Remove `sale-canary-1` from the LB | Ship `putIfAbsent` / `merge` / concurrent journal |
| Block promotion of 1.8.14 | Unique DB key on the JPA path before 100% traffic |
| Manual refund of documented duplicates (`harbor-8841`, `fog-coffee-2201`) | Metric `posts_per_key` paging before merchants do |
| Do not “fix” by lowering threads to 1 | Parallel harness in CI (Case A + Case B) |

## Evidence map (INC-JVM-201)

- Dashboard: throughput up, 5xx flat, `duplicate_payment_ratio` 1.8%, journal/min > distinct keys/min, JDBC 0.
- Logs: same key, two payment ids, two `HTTP_201 replay=false`; distinct keys sharing `journalSeq`.
- Timeline: canary 1.8.14 at 10% sale traffic.

## Common student misses

- Fixing only Case B (`putIfAbsent`) and leaving the lost update.
- Wrapping only the `ArrayList` and leaving the key race.
- Adding `synchronized` on the `String` account id.
- Declaring victory after one green run.

## Scoring note

A student who opens this file and copies `putIfAbsent` without a written hypothesis and three harness runs must not receive a high **Diagnostic method** score. Lucky or leaked answers can still earn Technical accuracy if the repair is correct; method is earned from evidence order.
