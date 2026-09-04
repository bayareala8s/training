# INCIDENT-403 — Instructor solution

**Do not share this file with students before they submit a worksheet.**

## RCA

Ledger writes no longer join the payment transaction.

`3.5.5-baypay.184` added `@Transactional(propagation = REQUIRES_NEW)` (JTA-equivalent: a new `UserTransaction`) on `PaymentPostingService.postAuthorized`. `create()` still commits `COMPLETED` on its own transaction. When posting hits a primary-key collision (`ledger_transactions_pkey`) it rolls back **only the posting unit**. The HTTP transaction already committed. Notifications still fire from the in-process event after `create()` returns.

Reference app (student laptop) does **not** have this annotation — the pack is a prod variant. Symptom matches “ledger write outside the JTA/Spring transaction or `REQUIRES_NEW` mismatch.”

UUID.randomUUID() per ledger attempt makes a retry a *different* id; it does not repair a split commit. The unique-violation count (6) matches missing coverage (6).

## Stabilization

1. Stop treating HTTP 201 as settlement truth. Finance uses ledger coverage, not API success.
2. Rollback to `3.5.5-baypay.181` **or** revert the posting annotation so posting joins `create()` again.
3. Pause or flag the six `COMPLETED` payments with `ledgerRows=0` (including `7c2a9e10-4b55-4d21-9a0e-0f3c1b77a901`). Do not auto-replay until you know whether money moved externally.
4. Do not “fix” by catching ledger failures and ignoring them.

## Remediation

- Restore `REQUIRED` / no annotation on `postAuthorized` while posting stays in-process.
- If posting must be isolated later, use an **outbox** (or a worker after commit) plus reconciliation — not a silent `REQUIRES_NEW` on the money write.
- Keep idempotency in the **same** unit as the payment insert.
- Add a coverage alert: `completed_count - ledger_payment_count` > 0.

## Evidence students should have used

| Gate | What it shows |
|---|---|
| Logs | `txn=committed` COMPLETED; ledger persist failed; `ledgerRows=0`; notification still sent |
| Dashboard | 100% coverage before 17:10, 96.7% after; pool healthy; HTTP 5xx = 0 |
| Deploy | BAYPAY-1844 `REQUIRES_NEW` on `postAuthorized`; `create()` unchanged |

## Comms (acceptable example)

SEV-2: six COMPLETED payments since 17:10 UTC have no ledger row, including Harbor Market / Avery Chen `7c2a9e10-…`. API returned 201. We are rolling back the 17:10 payment-service release and holding those six ids out of settlement until finance confirms. HTTP error rates were not a useful signal. Next update 20 minutes.

## Common wrong RCAs

- “Database is down” — writer CPU normal, HTTP 2xx.
- “Notification bug” — notifications firing is consistent with create having committed.
- “Idempotency failed” — not supported by the pack.
