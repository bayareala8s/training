# Deployment history — payment-service prod-east

**Gate:** 3  
**Synthetic BayPay. Change tickets are fictional.**

| When (UTC) | Version | Actor | Notes |
|---|---|---|---|
| 2026-08-18T15:02:00Z | 3.5.5-baypay.181 | deploy-bot | Routine; ledger coverage 100% for 72h after |
| 2026-08-20T22:40:00Z | 3.5.5-baypay.183 | deploy-bot | Config only (`leak-detection-threshold`). No Java change |
| 2026-08-21T17:10:00Z | 3.5.5-baypay.184 | Jordan Hale | Ticket BAYPAY-1844. Healthy at 17:12. One replica at a time |

## BAYPAY-1844 commit message (excerpt)

```
Isolate ledger posting from payment persist.

PaymentPostingService: add transaction demarcation so a ledger
failure cannot mark the HTTP create as failed.

Propagation set to REQUIRES_NEW on postAuthorized.
Idempotent ledger id uses UUID.randomUUID() per attempt.
```

## Files in 184 (from release notes)

- `transaction-worker/.../PaymentPostingService.java` — method-level transaction annotation added
- `payment-service/.../PaymentApplicationService.java` — unchanged `create()` still `@Transactional`
- No database migration

## Rollback

Version 181 is still tagged. Feature flag `baypay.posting.isolated` is **not** present; rollback is a redeploy.

## Operator comment (17:18 UTC)

> Posted a canary payment for Avery Chen. API 201, status COMPLETED. Did not wait for recon.
