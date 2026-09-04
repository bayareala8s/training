# Solution — BUILD-301 Payment REST API

Instructor only. Students should not need this to start the lab.

## Target

The production implementation is already the BayPay reference app:

- `reference-apps/baypay/payment-service/src/main/java/com/baypay/payment/api/PaymentController.java`
- `reference-apps/baypay/payment-service/src/main/java/com/baypay/payment/application/PaymentApplicationService.java`
- `reference-apps/baypay/payment-service/src/main/java/com/baypay/payment/api/CreatePaymentRequest.java`
- `reference-apps/baypay/shared/src/main/java/com/baypay/shared/idempotency/IdempotencyService.java`

A passing student rebuild matches this behavior even if line-for-line text differs.

## Status policy

```text
missing/invalid Idempotency-Key → 400 IDEMPOTENCY_KEY_REQUIRED
replay (same key + canonical hash) → 200 + original PaymentResponse
same key, different hash → 409 IDEMPOTENCY_CONFLICT
authorizer decline (frozen, currency, ceiling) → persist DECLINED, 422 body
new approved payment → post ledger, 201 + Location
GET unknown id → 404 PAYMENT_NOT_FOUND
```

The controller header is `required = false` so the service + `ApiExceptionHandler` own the `400` envelope.

## Canonical hash

```text
customerId|accountId|amount.toPlainString()|currency|reference-or-empty
```

Hashing raw JSON is a common student miss (`409` on identical retries).

## Constructor injection

`PaymentController(PaymentApplicationService)` only. No `new` of the service. `BayPayApplication` scans `com.baypay`.

## Validation command

```bash
cd reference-apps/baypay
./mvnw -pl payment-service -am -Dtest=PaymentApiIT test
```

All five methods in `PaymentApiIT` must pass, including OpenAPI path `/api/v1/payments`.

## Common gaps

| Symptom | Likely miss |
|---|---|
| Replay `201` | No `findReplay` or `CreateResult.replay` ignored |
| Decline `500` | Frozen account threw instead of `payment.decline` |
| Generic missing-header error | `required = true` on the header |
| `404` on POST mapping | Component scan too narrow |

## Rubric notes

Technical accuracy is the status matrix and idempotency store. Production awareness is decline persistence and correlation echo. Security/reliability is not logging PAN-like data and not skipping the key.
