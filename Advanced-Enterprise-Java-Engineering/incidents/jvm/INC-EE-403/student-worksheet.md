# INC-EE-403 student worksheet

Fill in order. Quote evidence. Do not paste instructor solutions.

**Incident:** Completed payment missing ledger row  
**Your name / cohort:**  
**Time started:** 2026-09-06  
**Time submitted:** 2026-09-06

## Current hypothesis

Gate 1: Payment `7c2a9e10-4b55-4d21-9a0e-0f3c1b77a901` is **COMPLETED** and **HTTP 201**. `PaymentApplicationService` logs `txn=committed`. **Then** `PaymentPostingService` fails `insert into ledger_transactions` (`ledger_transactions_pkey`) and marks **its** unit rollback-only. Recon: `ledgerRows=0`. Notify still ran (`PaymentCompletedEvent`). This is two units of work: payment committed, posting rolled back. The laptop reference app cannot do this (`postAuthorized` joins `create()`). The prod variant after 17:10 split the boundary. In-process notify is not proof the ledger committed. I have not yet named an annotation.

Gate 2: Not a pool or 5xx incident. After 17:10: 184 creates, **0** 5xx, readiness UP, Hikari 11/50, coverage **208/208 → 178/184 (96.7%)**. Notifications **184** = completed payments, not ledger rows. **6** unique violations on `ledger_transactions_pkey`, all after 17:10. Volume is healthy; the split is silent. Next: did deploy `.184` change posting’s transaction boundary?

Gate 3: Yes. BAYPAY-1844: “Isolate ledger posting… so a ledger failure cannot mark the HTTP create as failed. Propagation set to **REQUIRES_NEW** on `postAuthorized`.” `create()` still `@Transactional`. No migration. Ledger id is `UUID.randomUUID()` per attempt (not idempotent). Rollback is redeploy `.181`; no feature flag. Operator canary was 201/COMPLETED without waiting for recon.

## Supporting evidence

(File, timestamp, quote. Include payment id `7c2a9e10-4b55-4d21-9a0e-0f3c1b77a901` if you use it.)

| File | Quote |
|---|---|
| timeline.json 17:10 | `payment-service 3.5.5-baypay.184 marked healthy` |
| timeline.json 18:28 | Harbor Market HTTP 201 for `7c2a9e10-4b55-4d21-9a0e-0f3c1b77a901` |
| logs.txt 17:41:12.004 | `POST /api/v1/payments status=201 paymentId=7c2a9e10-…` |
| logs.txt 17:41:12.006 | `payment persisted status=COMPLETED … txn=committed` |
| logs.txt 17:41:12.019 | `ledger persist failed … constraint=ledger_transactions_pkey` |
| logs.txt 17:41:12.020 | `posting unit marked rollback-only` |
| logs.txt 17:41:12.031 | `PaymentCompletedEvent handled` (after ledger fail) |
| logs.txt 18:22:08 | `COMPLETED payment has no ledger row paymentId=7c2a9e10-… ledgerRows=0`; window `missingLedger=6` |
| dashboard.md | Coverage 100% → 96.7% after 17:10; 5xx = 0; 6 unique violations |
| deployment-history.md | `.184` `REQUIRES_NEW` on `postAuthorized`; `create()` unchanged |

## Next investigation

After gate 2: open deploy history for `.184` — did posting get its own transaction attribute, and is `create()` still one `@Transactional`? Gate 3 answered that. If live: `git show` `PaymentPostingService` on `.184`, `pg_stat` for the 6 PK errors, and a list of the 6 payment ids for finance hold. No thread dump required.

## Stabilization action

(How do you stop promising money you did not post? Replay? Flag? Freeze creates?)

- Redeploy **3.5.5-baypay.181** (or stop traffic to `.184`). Do not keep isolating posting.
- Give finance the 6 payment ids (`7c2a9e10-…`, `aa10bb20-…`, and recon’s other four). **Hold settlement** for those ids. Do not ship a file that treats HTTP 201 as posted.
- Do **not** tell Harbor Market to retry with a **new** Idempotency-Key (second `COMPLETED` if they later backfill). Same key replay is safe only after the code joins the transaction again.
- Do not “fix” by inserting random ledger UUIDs by hand without a written recon procedure.

## Remediation

- `postAuthorized` must **join** `create()` again (no `REQUIRES_NEW` on in-process posting). A ledger failure must fail the HTTP create (or roll it back) — FIX-304’s rule.
- If they want HTTP to return before the ledger exists, that is an **outbox in the same commit**, then a worker — not a second JTA unit that can die after `COMPLETED`.
- Ledger identity must be deterministic (e.g. payment id), not `randomUUID()` per attempt.
- Notify after commit of **ledger**, or from the worker. `PaymentCompletedEvent` in the same request is not a money guarantee.
- Coverage alert: `COMPLETED` count vs `PAYMENT` ledger rows, not 5xx.

## Communication update

(Five lines max. Audience: finance + merchant success. Do not name an annotation you have not shown.)

Since 17:10 UTC a subset of successful creates (`201`, status `COMPLETED`) have **no** `ledger_transactions` row. Example: `7c2a9e10-4b55-4d21-9a0e-0f3c1b77a901` (Avery / Harbor Market). Six rows in the 17:10–18:22 window. The payment save committed; the ledger write did not. We are rolling back the 17:10 release and holding settlement for those six ids. Do not retry those creates with a new key until finance confirms backfill. Next update in 15 minutes with the full id list.
