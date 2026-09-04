# BUILD-302 — Refund API

**Type:** BUILD  
**Module:** 3 — Spring Boot Engineering  
**Duration:** 60–90 minutes  
**Lessons:** [L-3.2](../../course/modules/03-spring-boot-engineering/lessons/L-3.2.md)

---

## Scenario

Merchants issue partial and full refunds against completed BayPay payments. You implement `POST /api/v1/refunds` and `GET /api/v1/refunds/{id}` on the same modular monolith so Avery Chen cannot be refunded more than she paid, and so a retried refund does not double-credit.

---

## Business context

Refunds are first-class money movement. A `$40` payment may take a `$15` partial refund and later a `$25` remainder. A `$12` full refund must mark the payment `REVERSED`. Over-refund is a finance incident. You extend `reference-apps/baypay/` (`refund-service` + the payment-service composition root). Do not stand up a second HTTP application.

---

## Learning objectives

- Rebuild or extend `RefundController` with constructor injection and `@Valid CreateRefundRequest`.
- Apply the same `Idempotency-Key` rules as payments (`201` / `200` / `409` / `400`).
- Reject refunds against non-refundable payment statuses (`422` `PAYMENT_NOT_REFUNDABLE`).
- Reject amounts that exceed remaining refundable (`422` `REFUND_EXCEEDS_REMAINING`).
- On a full refund, transition the payment to `REVERSED`.
- GET by id with `404` `REFUND_NOT_FOUND`.

---

## Architecture

```text
Merchant → RefundController → RefundApplicationService
                                 ├── PaymentRepository (must be COMPLETED or REVERSED)
                                 ├── RefundRepository (sum COMPLETED on that payment)
                                 ├── LedgerTransactionRepository
                                 └── IdempotencyService (REFUND_CREATE)
```

Refunds publish `RefundCompletedEvent` for `NotificationListener` in-process. Keep that in the same transaction as the reference app unless you are explicitly changing the consistency model (you are not, in this lab).

---

## Prerequisites

- BUILD-301 complete enough that you can create a `COMPLETED` payment.
- Java 21, Maven Wrapper, demo ids.

---

## Environment setup

```bash
export JAVA_HOME="${JAVA_HOME:-/opt/homebrew/opt/openjdk@21}"
cd reference-apps/baypay
./mvnw -pl payment-service -am test
./mvnw -pl payment-service -am spring-boot:run
```

Work in `com.baypay.refund.api` and `com.baypay.refund.application`. Reuse `shared` entities and `IdempotencyService.REFUND_CREATE`. If the reference implementation is present, rebuild the refund create path on a branch and use `RefundApiIT` as the spec.

---

## Challenge / tasks

1. Create a completed payment (BUILD-301 contract) as the source of funds.
2. Implement `POST /api/v1/refunds` with `paymentId`, `amount` (`>= 0.01`), optional `reason` (`@Size(max = 256)`), and `Idempotency-Key`.
3. Identical retry → `200` and the same `refundId`.
4. Partial refund leaves the payment `COMPLETED`. Additional refunds that exceed remaining → `422`.
5. Full refund → payment `REVERSED` (verify with `GET /api/v1/payments/{id}`).
6. Unknown payment id → `404` `PAYMENT_NOT_FOUND`. Unknown refund GET → `404` `REFUND_NOT_FOUND`.
7. Confirm `/v3/api-docs` includes `/api/v1/refunds`.

---

## Validation

```bash
cd reference-apps/baypay
./mvnw -pl payment-service -am -Dtest=RefundApiIT test
```

`RefundApiIT` creates its own payments. You should also walk the curl path: payment `201`, refund `201`, replay `200`, over-refund `422`, GET refund `200`.

---

## Troubleshooting

- `404` on `/api/v1/refunds` at the dispatcher: `scanBasePackages` omitted `com.baypay.refund`.
- Over-refund returns `201`: you did not sum `RefundStatus.COMPLETED` for that `paymentId` before save.
- Full refund leaves payment `COMPLETED`: missing `payment.transitionTo(REVERSED)` when remaining hits zero.
- Replay `409` on the same body: canonical hash must be `paymentId|amount|reason`, not pretty JSON.
- OpenAPI missing refunds: springdoc scans the same process; if the controller is a bean, the path appears.

---

## Expected outcome

`RefundApiIT` is green. A `$40` payment can take `$15` then reject `$30`. A `$12` payment becomes `REVERSED` after a `$12` refund. Replay is `200`.

---

## Interview questions

1. Why may a payment in `REVERSED` still accept a refund GET but not a new refund that exceeds remaining (which is zero)?
2. Why is refund idempotency a different `operation` string than payment create?
3. What should happen if two concurrent refunds each read remaining `$20` and both try `$15`?

---

## Architecture/trade-off questions

1. Should refund be a field on `Payment` instead of a separate resource?
2. When would refund posting become a message to `transaction-worker` instead of an in-process save?
3. Is `422` correct for over-refund, or would `409` be clearer? Defend one.

---

## Cleanup

Stop the running app. H2 data is discarded. No cloud resources.

---

## Cost estimate

**$0.**

---

## Hidden/revealable solution

When `RefundApiIT` has been run against your work, you may compare with `solutions/BUILD-302/`. Do not copy the remaining-amount check from the solution until you have failed or passed on your own sum.

---

## What you learned

- Refunds reuse the payment idempotency pattern with refund-specific domain codes.
- Remaining amount is a transactional read of completed refunds, not a column you decrement in the controller.
- Full refund is a payment state transition, not only a refund row.

---

## Portfolio deliverable

Add `RefundController` plus the remaining-amount rule to the Module 3 API excerpt. Note how a full refund changes payment status. This is the second half of the “payment and refund API” portfolio artifact.
