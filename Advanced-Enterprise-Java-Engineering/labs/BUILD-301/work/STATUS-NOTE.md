# BUILD-301 — Payment REST status note

Date: 2026-09-06  
App: `reference-apps/baypay` (already the composition root; no second Spring project)

## CreateResult → HTTP

`PaymentController.create` does not invent status. It maps `CreateResult`:

| Result | HTTP | Body |
|---|---|---|
| `replay == true` | **200** | Original payment, same `paymentId` |
| `status == DECLINED` | **422** | Saved payment (`failureReason` set) |
| First success | **201** + `Location` | `COMPLETED` after in-process post |

Header `Idempotency-Key` is `required = false` so a missing header reaches `IdempotencyKeys.require` → **400** `IDEMPOTENCY_KEY_REQUIRED`, not a Spring “required header” 400. Same key + different canonical hash → `IdempotencyConflictException` → **409**. GET missing id → **404** `PAYMENT_NOT_FOUND`.

Canonical hash fields: `customerId|accountId|amount.toPlainString()|currency|reference`.

## Why 201 / 200 / 422

**201** means this request created a new payment resource. The client may store `Location` / `paymentId`. Posting ran in the same `@Transactional` as authorize, so the body can honestly say `COMPLETED`.

**200** on an identical retry means “here is the resource you already created.” A second **201** would lie: we did not create a second debit. Finance treats two `COMPLETED` rows for one key as Sev-2. Replay consults `IdempotencyService.findReplay` *before* insert and does not call `PaymentPostingService` again.

**422** is a request we understood (valid JSON, known Avery, known frozen account) that the domain refused. We persist `DECLINED` so support can GET the id and see `account is not ACTIVE`. A **404** would say the account does not exist. A ProblemDetail-only **422** with no row makes the merchant retry with a new key and look like a new attempt with no audit. Bean Validation **400** stays for shape errors (`amount` &lt; 0.01, bad currency).

Constructor injection stops at the controller: it depends on `PaymentApplicationService`, not repositories. The service owns the key, the authorizer `Decision`, and the posting call.

## Evidence this sitting

- Live curl `Idempotency-Key: lab-301-invoice-1` → **201** `d03a56f9-…` `COMPLETED`, replay **200** same id, frozen `…222` → **422** `DECLINED`.
- `/v3/api-docs` lists `/api/v1/payments`.
- `PaymentApiIT` is the contract suite (create/replay, 409, 422, 400, OpenAPI).
