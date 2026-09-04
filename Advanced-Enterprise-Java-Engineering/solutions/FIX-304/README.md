# Solution — FIX-304 Transaction rollback bug

Instructor only. Do not walk the room to this text in the first 20 minutes.

## Root cause

`LeakyRefundService.create` saves a completed `Refund`, then wraps the ledger insert in `try/catch (Exception)`. On failure (including the injected `reason=force-ledger-failure`) it logs and **returns `CreateResult(refund, false)`**.

Consequences:

1. The caught exception never leaves the `@Transactional` proxy, so Spring **commits** the refund row.
2. The HTTP adapter treats the result as a successful create (`201`).
3. `ledger_transactions` has no matching `REFUND` (or has a row plus a later thrown failure — the starter throws after `save`, so a ledger row may exist in the same session **or** only the refund commits if `save` itself fails). With `force-ledger-failure`, `ledger.save` succeeds then `IllegalStateException` is swallowed — depending on flush timing you may see a ledger row in the persistence context that still commits with the refund, **or** students who change the throw to happen before save see refund-only. The pedagogical defect is the same: **success is returned after a ledger failure, and rollback does not run.**
4. Finance reconciliation breaks. A new `Idempotency-Key` can create another completed refund.

Default Spring rollback is for **propagating** `RuntimeException`. Swallowing is a commit.

## Correct behavior

Do not catch around the ledger write. Let `IllegalStateException` / `DataAccessException` propagate. The transaction rolls back: no completed refund, no partial ledger, HTTP `500` (or a mapped 503 if you add one). The client retries with the same key and does not observe a phantom refund.

Reference fix: [FixedRefundService.java](FixedRefundService.java). The healthy production class is `RefundApplicationService` (no swallow).

## How students should have proven it

1. Payment `201`, refund with `reason: force-ledger-failure` through the starter → HTTP success + GET refund `COMPLETED`.
2. Count `ledger_transactions` / notice the error log “Unable to post refund”.
3. Hypothesis: exception handled inside the transactional method.
4. Remove the catch (or rethrow). Same request → HTTP error, GET `404`, zero leftover refund.

## Validation

```bash
./mvnw -pl payment-service -am -Dtest=RefundApiIT test
```

Plus a student-written test that uses `force-ledger-failure` (or a failing `LedgerTransactionRepository` stub) and asserts rollback.

## What not to accept

- “Best-effort ledger” that still returns `201`.
- Compensating delete after commit as the only fix (discuss as a trade-off, do not score as a complete repair).
- Catching `Exception` and marking refund `FAILED` **without** rolling back other writes you intended to be atomic — better than silent success, still weaker than propagate + rollback.

## Rubric notes

Diagnostic method is the score that separates a lucky glance at `catch` from evidence (HTTP + counts + log). Technical accuracy is rollback restored. Communication is the one-page RCA without blaming Hibernate.
