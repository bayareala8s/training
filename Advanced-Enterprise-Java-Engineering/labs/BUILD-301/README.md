# BUILD-301 — Payment REST API

**Type:** BUILD  
**Module:** 3 — Spring Boot Engineering  
**Duration:** 60–90 minutes  
**Lessons:** [L-3.1](../../course/modules/03-spring-boot-engineering/lessons/L-3.1.md), [L-3.2](../../course/modules/03-spring-boot-engineering/lessons/L-3.2.md)

---

## Scenario

BayPay’s merchant app must create and fetch payments against the Enterprise Payment Platform. You implement `POST /api/v1/payments` and `GET /api/v1/payments/{id}` on the existing Spring Boot modular monolith so a retry cannot debit Avery Chen twice.

---

## Business context

Avery Chen (`11111111-1111-1111-1111-111111111111`) pays invoices from the active USD account (`22222222-2222-2222-2222-222222222221`). The frozen account (`…222`) must not authorize. Finance treats a second completed payment for one `Idempotency-Key` as a Sev-2. You work in `reference-apps/baypay/`. Do not start a new Spring Initializr project.

---

## Learning objectives

- Rebuild or extend `PaymentController` and the create path using constructor injection.
- Require `Idempotency-Key`; return `201` on first create, `200` on identical replay, `409` on key reuse with a new body.
- Return `422` with a `DECLINED` payment body for the frozen account.
- Return `400` `IDEMPOTENCY_KEY_REQUIRED` when the header is missing.
- Keep Bean Validation on `CreatePaymentRequest` and ProblemDetail errors.

---

## Architecture

```text
Merchant → PaymentController → PaymentApplicationService
                                  ├── IdempotencyService
                                  ├── PaymentAuthorizer
                                  ├── PaymentRepository / Account / Customer
                                  └── PaymentPostingService (same transaction)
```

Diagram: `AEJE-D-010` (Payment REST API request flow). Status policy is defined in L-3.2.

---

## Prerequisites

- Java 21 and the Maven Wrapper in `reference-apps/baypay`.
- Lessons L-3.1 and L-3.2.
- Familiarity with demo ids in [GETTING_STARTED.md](../../GETTING_STARTED.md).

---

## Environment setup

```bash
export JAVA_HOME="${JAVA_HOME:-/opt/homebrew/opt/openjdk@21}"
cd reference-apps/baypay
./mvnw -pl payment-service -am test
./mvnw -pl payment-service -am spring-boot:run
```

You implement against this app: `com.baypay.payment.api` and `com.baypay.payment.application`. Use types in `com.baypay.shared`. If the reference classes are already present, rebuild the controller and create path on a branch until you can explain every status without reading the solution.

---

## Challenge / tasks

1. Implement `POST /api/v1/payments` with `@Valid CreatePaymentRequest` and an optional `Idempotency-Key` header that the service still requires.
2. Persist a new payment through the existing authorizer and posting service. Happy path status is `COMPLETED`.
3. Identical key + canonical body → `200` and the original `paymentId`. Do not post a second ledger row.
4. Same key, different amount or reference → `409` `IDEMPOTENCY_CONFLICT`.
5. Frozen account → `422` and `status=DECLINED` (body is a payment, not only ProblemDetail).
6. Missing key → `400` `IDEMPOTENCY_KEY_REQUIRED`.
7. `GET /api/v1/payments/{id}` → `200` or `404` `PAYMENT_NOT_FOUND`.
8. Echo `X-Correlation-Id` (the existing filter is acceptable). Confirm `/v3/api-docs` lists `/api/v1/payments`.

---

## Validation

```bash
cd reference-apps/baypay
./mvnw -pl payment-service -am -Dtest=PaymentApiIT test
```

Manual smoke (app running):

```bash
curl -sS -D - -X POST http://localhost:8080/api/v1/payments \
  -H 'content-type: application/json' \
  -H 'Idempotency-Key: lab-301-invoice-1' \
  -H 'X-Correlation-Id: build-301' \
  -d '{
    "customerId":"11111111-1111-1111-1111-111111111111",
    "accountId":"22222222-2222-2222-2222-222222222221",
    "amount":25.00,
    "currency":"USD",
    "reference":"invoice-1001"
  }'
```

Expect `201` and `COMPLETED`. Replay the same command; expect `200` and the same `paymentId`. Repeat against the frozen account id with a new key; expect `422` and `DECLINED`.

---

## Troubleshooting

- Tests fail with `404` on `/api/v1/payments`: scan `com.baypay`, not only `com.baypay.payment`.
- Replay is `201`: you are not consulting `IdempotencyService.findReplay` before insert.
- `409` on an identical retry: you hashed raw JSON instead of a canonical string (`amount.toPlainString()`).
- Frozen account is `500`: exception escaped instead of `payment.decline` + `422`.
- Missing key is a generic Spring error: keep the header `required = false` and validate in `IdempotencyKeys.require`.

---

## Expected outcome

`PaymentApiIT` is green. Curl matches the status matrix. OpenAPI contains the payment path. You can explain `201` vs `200` vs `422` without opening a tutorial.

---

## Interview questions

1. Why is replay `200` rather than `201`?
2. Why persist a `DECLINED` payment instead of only returning ProblemDetail?
3. Where should constructor injection stop — controller, service, or repository?

---

## Architecture/trade-off questions

1. When would you move `PaymentPostingService` out of this request’s transaction?
2. Header `Idempotency-Key` versus a body field: which failure modes change?
3. Should GET accept an idempotency key? Why or why not?

---

## Cleanup

Stop the Spring Boot process (`Ctrl+C`). H2 is in-memory; there is nothing to destroy. Do not commit `target/` or local dumps.

---

## Cost estimate

**$0.** Local JVM and H2. No AWS.

---

## Hidden/revealable solution

Do not open instructor materials until `PaymentApiIT` has failed or passed on **your** code. A reference walkthrough lives at `solutions/BUILD-301/` (not linked as a shortcut from the tasks above). Compare status handling and the canonical hash after you have a result.

---

## What you learned

- Payment writes are a status policy plus a store, not “insert and return 201.”
- Bean Validation and domain decline are different HTTP meanings.
- The BayPay app is the stack; labs extend it.

---

## Portfolio deliverable

Export your `PaymentController` create method, the `CreateResult` status mapping, and a short note (half page) defending `201` / `200` / `422`. This excerpt feeds the Module 3 portfolio artifact (payment + refund API).
