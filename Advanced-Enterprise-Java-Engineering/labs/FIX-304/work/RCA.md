# FIX-304 — Refund / ledger split

Date: 2026-09-06  
Did not open `solutions/FIX-304` before the hypothesis.

## Symptoms

Merchant `POST /api/v1/refunds` → **201** and a `refundId`. GET refund → `COMPLETED`. Nightly `ledger_transactions` extract has **no** `REFUND` row for that id.

## Hypothesis (before changing the healthy path)

`LeakyRefundService` saves and completes the refund, then wraps the ledger write in `try/catch (Exception)`. On failure it logs and **returns** `CreateResult(refund, false)`. Spring `@Transactional` rolls back only when a runtime exception **leaves** the method. Catching it commits the refund. The controller maps that to **201**. Support can GET the row. Treasury cannot.

`force-ledger-failure` after a successful `ledger.save` still posts a row; the real split is `ledger.save` itself throwing (or the catch around it).

## Evidence

`LeakyRefundReproduceIT` (profile `leaky`): spy throws on `REFUND` save. Leaky `create` returns a `COMPLETED` refund. `refunds` has the row. `findByRefundId` is empty.

## Fix

Leave `RefundApplicationService` as the `local` / `test` bean. Do not catch ledger failures. `RefundLedgerRollbackIT`: same spy, HTTP **500**, zero `COMPLETED` refunds for that payment, zero `REFUND` ledger rows.

`LeakyRefundService` is `@Profile("leaky")` only. Starter under `labs/FIX-304/starter` is unchanged.

## Prevention

A successful refund HTTP response means the refund row **and** the `REFUND` ledger row committed together. Compensating “delete the refund later” is not the default. If posting moves to a worker, use an outbox in the same commit, not catch-and-return-201.
