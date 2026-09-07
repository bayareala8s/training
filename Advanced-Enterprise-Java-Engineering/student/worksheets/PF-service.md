# Portfolio — BayPay payment service (list-by-customer)

**Artifact:** [CAPSTONE-1](../../capstones/01-build-baypay/README.md)  
**Course:** Advanced Enterprise Java Engineering  
**Case study:** BayPay Financial Services (fictional)  
**After:** Modules 1–3  
**Diagram:** AEJE-D-071 (current WebSphere estate — cite as what you did **not** rebuild)  
**Reference app:** `reference-apps/baypay` (Java 21, Spring Boot 3.5.5)

Export this page (or a copy) as your CAPSTONE-1 portfolio artifact. Fill every section in your own words. Do not paste instructor solution text. Do not put PAN, CVV, access keys, or `BAYPAY_DB_PASSWORD` in this file.

**Your name:**  
**Date:** 2026-09-07  
**Cohort / reviewer (if any):**  
**Reference commit / branch:** Downloads working tree (not pushed)

---

## 1. Baseline proof

Record the command you ran **before** you claimed the list was done.

| Field | Your answer |
|---|---|
| `JAVA_HOME` you used | `/opt/homebrew/opt/openjdk@21` |
| Working directory | `reference-apps/baypay` |
| Command (`./mvnw test`) | `./mvnw -pl payment-service -am test` then full `./mvnw test` |
| Result (green / red, suite names) | Green. Shared unit tests + `PaymentApiIT` (5) + new `PaymentListApiIT` (7) + refund/ledger/health ITs. `BUILD SUCCESS`. |
| `PaymentApiIT` still green after your list? | Yes — create `201`, replay `200`, conflict `409`, frozen `422`, missing key `400`, OpenAPI still published. |

One paragraph: what was already true about POST create and GET by id before you added anything.

`PaymentController` already owned `POST /api/v1/payments` and `GET /api/v1/payments/{paymentId}`. Create went through `IdempotencyService` (same key + same canonical body → replay `200`; same key + different body → `409 IDEMPOTENCY_CONFLICT`), `PaymentAuthorizer` (frozen `…222` → persisted `DECLINED` + `422`), and `PaymentPostingService` so a happy path returned `COMPLETED` on the first response. GET-by-id loaded one row or threw `PAYMENT_NOT_FOUND`. Bean Validation already sat on `CreatePaymentRequest`. None of that is a statement screen: Harbor Market cannot ask “show Avery Chen’s payments” without knowing every `paymentId` in advance.

---

## 2. The gap you named

`PaymentController` shipped with POST create and GET by id. It did **not** list by customer.

| Field | Your answer |
|---|---|
| File you opened first | `payment-service/.../api/PaymentController.java` |
| Methods you found | `create(...)` and `get(@PathVariable UUID paymentId)` — no collection GET |
| Repository methods you found | `PaymentRepository`: `findById` (from `JpaRepository`) and `findByIdempotencyKey`. No `findByCustomerId…`. `CustomerRepository` is `findById` only. |
| Why Harbor Market cannot use GET-by-id alone for Avery’s statement | Finance has Avery’s customer UUID, not a bag of payment ids. GET-by-id is a single-resource read. A statement is a filtered collection. Guessing ids or scanning H2 is not a contract. |

Avery Chen `11111111-1111-1111-1111-111111111111` · active account `22222222-2222-2222-2222-222222222221` · frozen `22222222-2222-2222-2222-222222222222`.

---

## 3. List-by-customer contract

Cite the path `GET /api/v1/payments?customerId=`.

| Case | Status + body you implemented | Test name |
|---|---|---|
| Avery with two (or more) payments | `200` JSON array of `PaymentResponse`; both `paymentId`s present | `PaymentListApiIT.listsAveryPaymentsNewestFirst` |
| Known customer, zero payments | `200` `[]` (seeded idle customer in the IT, not a fake Avery) | `PaymentListApiIT.knownCustomerWithNoPaymentsReturnsEmptyArray` |
| Missing `customerId` | `400` Problem Detail `VALIDATION_FAILED` | `PaymentListApiIT.missingCustomerIdIs400` |
| Unparseable UUID | `400` `VALIDATION_FAILED` | `PaymentListApiIT.unparseableCustomerIdIs400` |
| Unknown customer UUID | `404` `CUSTOMER_NOT_FOUND` | `PaymentListApiIT.unknownCustomerIs404` |
| Sort (teaching: newest first) | `createdAt` descending; newer `paymentId` has a lower index than older | same list test (relative order, not `$[0]/$[1]`, because H2 is shared with `PaymentApiIT`) |

Bean Validation (or equivalent) — where does it live, and what handler returns `400`?

`@Validated` on `PaymentController`. `customerId` is `@RequestParam(required = false) @NotNull` so a missing query hits method validation instead of a silent “list everyone.” `ApiExceptionHandler` maps `HandlerMethodValidationException` / `ConstraintViolationException` / `MethodArgumentTypeMismatchException` / `MissingServletRequestParameterException` to the same `VALIDATION_FAILED` envelope already used for `@Valid CreatePaymentRequest`. I did not invent a default UUID.

Why is there **no** unfiltered `GET /api/v1/payments`?

A collection without a customer is an admin dump of H2. Harbor Market’s console is Avery’s statement, not every merchant payment in the teaching database. An unfiltered list is also the wrong default if a query param is forgotten — that is a `400`, not friendliness.

---

## 4. POST contracts you refused to drop

| Contract | Still true? (yes/no + evidence) |
|---|---|
| `Idempotency-Key` required | Yes — `PaymentApiIT.requiresIdempotencyKey` and `PaymentListApiIT.postStillRequiresIdempotencyKey` |
| First create `201` + `COMPLETED` (happy path) | Yes — `PaymentApiIT.createsCompletedPaymentAndReplaysIdempotentRetry` |
| Identical replay `200` + same `paymentId` | Yes — same test; list is not a second write |
| Same key, different body `409` `IDEMPOTENCY_CONFLICT` | Yes — `PaymentApiIT.rejectsReusedKeyWithDifferentBody` |
| Frozen account `422` + `DECLINED` | Yes — `PaymentApiIT.declinesFrozenAccount` |
| Missing key `400` `IDEMPOTENCY_KEY_REQUIRED` | Yes — header still `required = false` on the mapping; service calls `IdempotencyKeys.require` |
| GET by id `200` / `404` `PAYMENT_NOT_FOUND` | Yes — GET `/{paymentId}` unchanged; missing row still `ResourceNotFoundException` → `PAYMENT_NOT_FOUND` |

Canonical hash string (field order):

```text
customerId|accountId|amount.toPlainString()|currency|reference-or-empty
```

---

## 5. Logs you refused

| Field or habit | Why you refused it |
|---|---|
| PAN / full card number | Compliance incident, not a debug convenience. This API never accepts a card field; I did not add one “for the list.” |
| CVV / expiry | Same. Not on `CreatePaymentRequest`; not invented on the list query. |
| Raw create JSON `toString()` | The body is the closest thing we have to a card-shaped payload. Hash the canonical fields; do not log the JSON. |
| Dumping every payment row to INFO | A statement screen is a read. INFO-dumping Avery’s history is a PII leak waiting for a log aggregator. |

What you **do** log (paymentId, correlation id, status):

Existing structured fields stay: `paymentId`, `X-Correlation-Id` (filter already echoes it), status / audit action. List path does not log the query body. Customer UUID may appear in a not-found message; that is not a PAN.

One paragraph: why Avery’s UUID on a list query is not a PAN, and why that still does not belong on a Micrometer label in later modules.

Avery’s id is a synthetic primary key (`11111111-…1111`), not a 13–19 digit card number or track. It is safe to put on the query string and in a 404 detail. It is still a high-cardinality identifier. Tagging `payment.create` or a list counter with `customerId` is the Module 13 cardinality incident — the list contract does not get a free pass to become a label.

---

## 6. Estate you did not rebuild

Cite **AEJE-D-071**. Traditional ND is the source estate.

| Locked name | What it is | Why it is not this capstone’s runtime |
|---|---|---|
| `BayPayCell` | Traditional WebSphere cell on the leftover drawing | List runs in `reference-apps/baypay` on Boot 3.5.5 / Java 21 / H2 |
| `dmgr-east` | Deployment manager of that cell | No ND install; no bounce; no ear deploy |
| `PaymentCluster` | Cluster that used to host `payment.ear` | Collection GET is a controller method, not a new ear on Pay1 |
| `ihs-east` | IHS in front of the leftover cell | Local teaching edge is `localhost:8080` / MockMvc |

One sentence: what you would tell Jordan Voss who asks for “an ear on Pay1 so the list matches the diagram.”

The diagram is inventory of the estate we are leaving; Harbor Market’s statement is a Boot read next to the create you already accepted — a second ear on `PaymentCluster` would be building AEJE-D-071 instead of shipping the API.

---

## 7. Excerpt (short)

Paste **only** the list method signature plus five to fifteen lines, or describe it. No full module dump. No secrets.

```text
@GetMapping
public List<PaymentResponse> list(
        @RequestParam(required = false) @NotNull UUID customerId) {
    return payments.listByCustomer(customerId).stream()
            .map(PaymentResponse::from)
            .toList();
}

// PaymentApplicationService.listByCustomer:
//   customers.findById → CUSTOMER_NOT_FOUND
//   payments.findByCustomerIdOrderByCreatedAtDesc
```

IT class and method names you added:

`PaymentListApiIT`: `listsAveryPaymentsNewestFirst`, `knownCustomerWithNoPaymentsReturnsEmptyArray`, `missingCustomerIdIs400`, `unparseableCustomerIdIs400`, `unknownCustomerIs404`, `postStillRequiresIdempotencyKey`, `openApiListsCustomerIdQuery`.

---

## 8. Interview snippet (Staff, 6–8 sentences)

Harbor Market already had create and get-by-id. Finance asked for Avery Chen’s statement, so we added `GET /api/v1/payments?customerId=` on the same `PaymentController` — newest `createdAt` first, `PaymentResponse[]`, known-empty `200 []`, unknown customer `404 CUSTOMER_NOT_FOUND`, missing or garbage query `400 VALIDATION_FAILED`. There is no unfiltered list; forgetting `customerId` is not “list H2.” POST still requires `Idempotency-Key` because a retry with the same key is a Sev-2 if it debits twice; the list is a read and does not carry the key. Replay stays `200` with the original `paymentId`; conflict stays `409`; frozen `…222` stays `422 DECLINED`. We did not log PAN, CVV, or the create JSON to “debug the list.” AEJE-D-071 still shows merchants → `ihs-east` → `PaymentCluster` → `db-east`; that is the leftover ND cell, not this runtime. Jordan, we are not putting an ear on Pay1 so the list matches the drawing.

---

## Honesty

- [x] I ran `./mvnw test` in `reference-apps/baypay` with Java 21 / `JAVA_HOME`
- [x] I did not open `solutions/CAPSTONE-1/` before I had my own list test
- [x] I did not paste instructor Java as my only implementation
- [x] POST still requires `Idempotency-Key`
- [x] I did not log PAN, CVV, or a live password
- [x] I did not install WebSphere ND or put the list on `PaymentCluster`
- [x] I did not create a second Spring app
- [x] I did not set `-Xmx` equal to a container / cgroup limit as the run story
