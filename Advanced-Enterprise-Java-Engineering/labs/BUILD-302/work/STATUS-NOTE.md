# BUILD-302 — Refund REST status note

Date: 2026-09-06  
Same process as BUILD-301. `refund-service` is a Maven module, not a second HTTP app.

## Controller mapping

`RefundController.create` maps `CreateResult` the same way as payments: replay → **200**, first create → **201** + `Location`. Currency is taken from the payment, not the JSON body.

Canonical hash: `paymentId|amount.toPlainString()|reason` under operation `REFUND_CREATE`. A payment key reused as a refund key is a different operation row.

## Remaining-amount rule

Sum `RefundStatus.COMPLETED` for that `paymentId`. If `sum + request > payment.amount` → throw `REFUND_EXCEEDS_REMAINING` (**422** ProblemDetail, no refund row). Partial `$15` on `$40` leaves payment `COMPLETED`. `$30` more is refused. When `sum + request == payment.amount`, `payment.transitionTo(REVERSED)` — original amount stays on the payment.

`REVERSED` is still a refundable *status* so a late replay is not a confusing `PAYMENT_NOT_REFUNDABLE`. A new amount that exceeds remaining (now zero) is still **422**. GET of an existing refund remains **200**.

## Why not a field on Payment

A refund is its own resource with its own key, ledger `REFUND` row, and GET. Remaining is a transactional read of completed refunds, not a column the controller decrements.

## Concurrent `$15` + `$15` against `$20` remaining

Both threads can read remaining `$20` unless the unit of work serializes. This monolith relies on one `@Transactional` plus row locking / unique key — not a heap remaining field. Two winners would violate finance; the unique refund key only stops *retries of the same request*, not two different keys. Production needs the remaining check inside the same transaction that inserts the refund (and, under load, a constraint or lock on the payment row).

## Why 422 not 409 for over-refund

**409** here is “same idempotency key, different body.” Over-refund is a understood request the domain refuses — same family as frozen-account decline. **422**.

## Evidence this sitting

- `RefundApiIT` 2/2.
- `$40` payment `e1fccb01-…` → refund `$15` **201** `b090ecbd-…` → replay **200** → `$30` **422** `REFUND_EXCEEDS_REMAINING` → payment still `COMPLETED`.
- `$12` payment `88d23d98-…` → refund `$12` **201** → payment `REVERSED`.
- Ghost payment **404** `PAYMENT_NOT_FOUND`; ghost GET **404** `REFUND_NOT_FOUND`; missing key **400**.
