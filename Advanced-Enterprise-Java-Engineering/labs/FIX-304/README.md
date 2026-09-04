# FIX-304 — Transaction rollback bug

**Type:** BREAK/FIX  
**Module:** 3 — Spring Boot Engineering  
**Duration:** 60–90 minutes  
**Lessons:** [L-3.4](../../course/modules/03-spring-boot-engineering/lessons/L-3.4.md)

This lab does **not** include the root cause. Diagnose from symptoms and the starter, then fix the refund path on the BayPay app.

---

## Scenario

BayPay finance opened an incident: several refunds show as successful in the merchant API, but nightly reconciliation cannot find matching ledger postings. You are given a starter service used in a feature branch. Reproduce the disagreement, find why API and ledger diverge, and restore atomic refund behavior.

---

## Business context

Avery Chen received a `$40` payment (`COMPLETED`) and requested a `$15` refund. The HTTP client stored a `201` and a `refundId`. The general ledger extract for that day has no `REFUND` row for that id. Customer support can GET the refund. Treasury cannot. Until this is fixed, BayPay must not expand refund volume.

Work in `reference-apps/baypay/`. Replace or wrap the refund application path with the starter, then correct it. Do not build a new service.

---

## Learning objectives

- Reproduce an API-success / ledger-missing refund using the starter.
- Form a hypothesis from logs, HTTP status, and table contents (not from a guessed one-liner).
- Restore the invariant: a successful refund response implies a persisted ledger refund in the same commit, or the client sees failure and **no** completed refund row.
- Re-run `RefundApiIT` and a failure-injection check you design.

---

## Architecture

```text
POST /api/v1/refunds → refund application path → payments / refunds / ledger_transactions
```

The healthy reference path is `RefundApplicationService`. The suspect branch code is [starter/LeakyRefundService.java](starter/LeakyRefundService.java). Wire the starter in place of the healthy service (or call it from a temporary controller hook), observe, then fix.

Diagram: `AEJE-D-013` (do not treat the diagram filename as the diagnosis).

---

## Prerequisites

- L-3.4 and BUILD-303 (you need to query `refunds` and `ledger_transactions`).
- Ability to run `RefundApiIT`.

---

## Environment setup

```bash
export JAVA_HOME="${JAVA_HOME:-/opt/homebrew/opt/openjdk@21}"
cd reference-apps/baypay
```

Copy the starter into the refund application package (or keep it side-by-side) and point the refund controller at it. Use profile `local` or `test`. Seeded Avery Chen identities still apply.

---

## Challenge / tasks

1. Create a completed payment, then drive a refund through the starter.
2. Record HTTP status, refund GET body, and SQL counts for `refunds` versus `ledger_transactions` for that payment.
3. Read the starter. Note control flow around the ledger write. Write a hypothesis **before** you change code.
4. Change only what is required so a ledger failure cannot produce a successful refund HTTP response with a committed refund row.
5. Confirm happy-path `RefundApiIT` still passes on the fixed path.
6. Add or run a test that forces a ledger write failure and expects **no** committed completed refund (HTTP error, empty or rolled-back refund row).

Do not ask the instructor for the cause in the first 20 minutes.

---

## Validation

Happy path:

```bash
./mvnw -pl payment-service -am -Dtest=RefundApiIT test
```

Incident path (your check): after a forced ledger failure, `GET /api/v1/refunds/{id}` must not return a completed refund that lacks a ledger row. A `5xx` or domain error **and** zero leftover completed refund rows is the passing incident result.

---

## Troubleshooting

- Cannot see tables: use H2 console on `local`, or `JdbcTemplate` in a test.
- Controller still calls `RefundApplicationService`: you did not swap the bean. Use `@Primary`, a profile, or temporarily change the controller constructor type.
- Tests pass but finance still would fail: you fixed the happy path only; inject a ledger failure.
- Everything 404s: component scan / bean not picked up.

---

## Expected outcome

You have a written hypothesis, a fix, green `RefundApiIT`, and a failure-injection test that proves refund and ledger stay aligned. You can explain the before/after in an incident update without blaming “JPA is weird.”

---

## Interview questions

1. How do you prove API and ledger disagree without reading the service first?
2. What HTTP status should a client see when posting fails after a refund row was written in the same unit of work?
3. Which log fields would you require in the Sev-2 channel update?

---

## Architecture/trade-off questions

1. Should ledger post stay in the refund HTTP transaction, or move to an outbox?
2. What does a modular monolith still owe finance if you extract `transaction-worker` next quarter?
3. Is a compensating “delete the refund row” job an acceptable alternative to rolling back? When?

---

## Cleanup

Remove the starter bean from the running configuration so the healthy `RefundApplicationService` is what `main` uses. Stop the JVM. Do not commit a broken `@Primary` into the shared branch.

---

## Cost estimate

**$0.**

---

## Hidden/revealable solution

Instructor analysis and a reference fix live under `solutions/FIX-304/` and are **not** described here. Open them only after you have a hypothesis and a failing or passing incident test. This README will not confirm or deny your first guess.

---

## What you learned

- Reconciliation incidents are table-versus-HTTP problems.
- Diagnosis comes from evidence (status, counts, logs), then a code change.
- The BayPay refund path must keep money rows aligned.

---

## Portfolio deliverable

A one-page RCA: symptoms, evidence, hypothesis, fix, prevention. Do not paste the starter. This note supports later concurrency/RCA portfolio work and Capstone 1 review.
