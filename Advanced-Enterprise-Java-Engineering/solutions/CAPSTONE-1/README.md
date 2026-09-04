# CAPSTONE-1 — Instructor solution

**Do not share these files with students before they have a list test of their own.**

`hideAnswerUpfront` is false on the student guide, so they may see a **checklist**. This folder is the answer key. A student implementation that matches the contracts passes even if method names or sort APIs differ.

## What the reference app already does

`PaymentController` in `reference-apps/baypay/payment-service` already has:

- `POST /api/v1/payments` with `@Valid CreatePaymentRequest` and `Idempotency-Key` (`required = false` on the header; `IdempotencyKeys.require` owns `400 IDEMPOTENCY_KEY_REQUIRED`)
- `GET /api/v1/payments/{paymentId}` → `PaymentResponse` or `404 PAYMENT_NOT_FOUND`

There is **no** collection GET. `PaymentApplicationService` has `create` and `get`. `PaymentRepository` has `findById` and `findByIdempotencyKey` only.

`PaymentApiIT` already locks create `201`, replay `200`, conflict `409`, frozen `422` + `DECLINED`, missing key `400`, and OpenAPI paths for payments and refunds.

Students must keep all of that. The new work is list-by-customer plus tests plus PF-service.md.

## Status policy (writes unchanged)

```text
missing/invalid Idempotency-Key → 400 IDEMPOTENCY_KEY_REQUIRED
replay (same key + canonical hash) → 200 + original PaymentResponse
same key, different hash → 409 IDEMPOTENCY_CONFLICT
authorizer decline (frozen, currency, ceiling) → persist DECLINED, 422 body
new approved payment → post ledger, 201 + Location
GET unknown payment id → 404 PAYMENT_NOT_FOUND
```

Canonical hash remains:

```text
customerId|accountId|amount.toPlainString()|currency|reference-or-empty
```

## List-by-customer contract

```text
GET /api/v1/payments?customerId={uuid}
  known customer, 0..n payments → 200 JSON array of PaymentResponse
  sort teaching default → createdAt descending (newest first)
  missing customerId → 400 VALIDATION_FAILED (or equivalent ProblemDetail)
  unparseable UUID → 400
  unknown customer UUID → 404 CUSTOMER_NOT_FOUND
  no unfiltered GET /api/v1/payments
GET /api/v1/payments/{paymentId} unchanged
```

Empty array means “this customer exists and has no payments,” not “we did not look up the customer.”

Avery Chen is `11111111-1111-1111-1111-111111111111`. Active account `22222222-2222-2222-2222-222222222221`. Frozen `22222222-2222-2222-2222-222222222222`.

## Optional Java sketch

Comment-form copy: [ListPaymentsSnippet.java](ListPaymentsSnippet.java). Students may name methods differently. This sketch matches existing packages, constructor injection, and `ErrorCode`.

`PaymentRepository` — add a derived query (Spring Data JPA is already on the interface):

```java
List<Payment> findByCustomerIdOrderByCreatedAtDesc(UUID customerId);
```

`PaymentApplicationService` — read-only list after a customer existence check:

```java
@Transactional(readOnly = true)
public List<Payment> listByCustomer(UUID customerId) {
    customers.findById(customerId)
            .orElseThrow(() -> new ResourceNotFoundException(
                    ErrorCode.CUSTOMER_NOT_FOUND, "Customer not found: " + customerId));
    return payments.findByCustomerIdOrderByCreatedAtDesc(customerId);
}
```

`PaymentController` — collection mapping beside GET-by-id. Annotate the controller with `@Validated` if you put `@NotNull` on `@RequestParam`. `MethodArgumentNotValidException` alone will not fire for a missing query.

```java
@GetMapping
@Operation(summary = "List payments for a customer")
public List<PaymentResponse> list(@RequestParam @NotNull UUID customerId) {
    return payments.listByCustomer(customerId).stream()
            .map(PaymentResponse::from)
            .toList();
}
```

If `@NotNull` on the query does not produce `400`, handle `ConstraintViolationException` next to `MethodArgumentNotValidException` in `ApiExceptionHandler` with `ErrorCode.VALIDATION_FAILED` and ProblemDetail. Missing query must not become “list all.”

Do not add `Idempotency-Key` to the list. GET is not a write.

## Tests instructors expect

Extend `PaymentApiIT` or add `PaymentListApiIT` in the same package. Minimum:

1. Two POSTs for `DemoIds.CUSTOMER_AVERY` / `DemoIds.ACCOUNT_ACTIVE` with distinct keys and references → `GET ?customerId=` includes both `paymentId`s.
2. Newest-first: create an older payment then a newer one; first array element is the later payment (or assert both ids and relative order).
3. `GET /api/v1/payments` with no query → `400`.
4. `GET ?customerId=` with a random UUID that is not seeded → `404` and `$.code` `CUSTOMER_NOT_FOUND`.
5. Existing `createsCompletedPaymentAndReplaysIdempotentRetry` and `requiresIdempotencyKey` still green.

OpenAPI: `$.paths['/api/v1/payments'].get` exists and documents `customerId` if they already assert POST/GET-by-id on `/v3/api-docs`.

## Logging / PAN

`ApiExceptionHandler` already logs URI on unhandled errors, not the body. Fail Security / reliability if the student adds `log.info("{}", request)` on create or list, logs a PAN/CVV field, or prints the raw JSON. Allowed: `paymentId`, customer UUID, status, `X-Correlation-Id`. Avery’s UUID in an application log is acceptable; a card number is not.

## What this capstone is not

- Not a new Spring app.
- Not a rebuild of AEJE-D-071 (`BayPayCell`, `dmgr-east`, `PaymentCluster`, `ihs-east`).
- Not a pagination platform. A simple array is enough.
- Not a Module 9/10 container lab. Do not require Docker. Never teach `-Xmx` equal to a cgroup limit here.

## Validation command

```bash
export JAVA_HOME="${JAVA_HOME:-/opt/homebrew/opt/openjdk@21}"
cd reference-apps/baypay
./mvnw test
```

## Scoring notes

Technical accuracy is the list contract **and** the unchanged POST matrix. Diagnostic method is “proved `./mvnw test`, named the gap, then added tests.” Production awareness is newest-first, `404` vs `[]`, and AEJE-D-071 as estate they refused. Security / reliability is the key on POST plus no PAN in logs. Communication is PF-service.md. Opening this folder before a student list test caps Diagnostic method.

A pretty list that drops `Idempotency-Key` from POST cannot pass. A green `./mvnw test` with no list method cannot pass.
