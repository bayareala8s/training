# Solution — BUILD-302 Refund API

Instructor only.

## Target

- `reference-apps/baypay/refund-service/src/main/java/com/baypay/refund/api/RefundController.java`
- `reference-apps/baypay/refund-service/src/main/java/com/baypay/refund/application/RefundApplicationService.java`
- `reference-apps/baypay/refund-service/src/main/java/com/baypay/refund/api/CreateRefundRequest.java`

Same process as payments: `payment-service` is the composition root. `RefundController` must be scanned via `com.baypay`.

## Domain rules

1. Payment must exist (`404` `PAYMENT_NOT_FOUND`).
2. Payment status must be `COMPLETED` or `REVERSED` (`422` `PAYMENT_NOT_REFUNDABLE`).
3. Sum of `RefundStatus.COMPLETED` for that payment plus the new amount must not exceed `payment.money().amount()` (`422` `REFUND_EXCEEDS_REMAINING`).
4. Persist refund `COMPLETED`, ledger type `REFUND`, transaction event, audit, idempotency `REFUND_CREATE`.
5. If remaining becomes zero, `payment.transitionTo(REVERSED)` and save.
6. Publish `RefundCompletedEvent` (in-process notification).

## HTTP policy

Identical to payments: `201` create, `200` replay, `409` conflict, `400` missing key. GET unknown refund → `404` `REFUND_NOT_FOUND`.

Canonical hash:

```text
paymentId|amount.toPlainString()|reason-or-empty
```

Operation string must be `IdempotencyService.REFUND_CREATE`, not `PAYMENT_CREATE`, or keys collide across resources.

## Validation command

```bash
cd reference-apps/baypay
./mvnw -pl payment-service -am -Dtest=RefundApiIT test
```

`refundsCompletedPaymentAndBlocksOverRefund` and `fullRefundReversesPayment` are the bar.

## Common gaps

| Symptom | Likely miss |
|---|---|
| `$15` then `$30` both `201` | No remaining-amount sum |
| Full refund, payment still `COMPLETED` | Missing `REVERSED` transition |
| Dispatcher `404` on `/api/v1/refunds` | Scan base package |
| Replay `409` | JSON hash / wrong operation name |

## Rubric notes

Score remaining-amount as technical accuracy. Score “refund is its own resource + operation key” as trade-off/architecture. Security/reliability: do not refund `DECLINED` or `FAILED` payments.
