# BUILD-303 — Persistence

**Type:** BUILD  
**Module:** 3 — Spring Boot Engineering  
**Duration:** 60–90 minutes  
**Lessons:** [L-3.4](../../course/modules/03-spring-boot-engineering/lessons/L-3.4.md)

---

## Scenario

BayPay’s HTTP API is only as true as the tables behind it. You implement or extend JPA entities and Spring Data repositories in `shared` so payments, refunds, and ledger rows survive a process restart on PostgreSQL and remain usable on H2 for local work.

---

## Business context

Finance reconciles `payments` to `ledger_transactions`. A completed payment without a ledger row, or a mapping that works on H2 and fails on PostgreSQL reserved words, becomes a Monday incident. You stay inside `reference-apps/baypay/`. Do not introduce MongoDB, Redis, or a second schema “for practice.”

---

## Learning objectives

- Map `Payment`, `Refund`, and `LedgerTransaction` with embedded `Money`, STRING enums, and `@Version` where the reference app uses it.
- Provide `PaymentRepository` and `RefundRepository` finders used by the application services.
- Keep `open-in-view: false` and `@Transactional` on use cases.
- Run the default suite on H2 (`MODE=PostgreSQL`) and, if Docker is available, `PostgresCompatibilityIT`.
- Explain `ddl-auto: update` (local) versus `validate` (prod).

---

## Architecture

```text
shared (entities + repositories)
   ↑
payment-service / refund-service / transaction-worker  (same DataSource, same TM)
```

Local: H2 mem `baypay`, `ddl-auto: update`. Test: H2 `baypaytest`, `create-drop`. Prod: PostgreSQL, `validate`. Optional: Testcontainers `postgres:16-alpine`.

Diagram: `AEJE-D-011` (JPA transaction boundary).

---

## Prerequisites

- L-3.4. BUILD-301/302 recommended so you have rows to inspect.
- Java 21. Docker only if you want the Postgres IT.

---

## Environment setup

```bash
export JAVA_HOME="${JAVA_HOME:-/opt/homebrew/opt/openjdk@21}"
cd reference-apps/baypay
./mvnw -pl shared,payment-service -am test
```

Inspect `application-local.yml`, `application-test.yml`, and `application-prod.yml`. Entities live under `com.baypay.shared.domain`; repositories under `com.baypay.shared.persistence`.

If you rebuild mappings, do it on a branch against these packages — not a new persistence module.

---

## Challenge / tasks

1. Ensure `Payment` maps to `payments` with unique `idempotencyKey`, embedded amount/currency, STRING `status`, and `@Version`.
2. Ensure `Refund` maps similarly on `refunds`, with `findByPaymentIdAndStatus`.
3. Ensure `LedgerTransaction` maps to `ledger_transactions` with type `PAYMENT` or `REFUND`.
4. Confirm `@EntityScan` / `@EnableJpaRepositories` use `com.baypay`.
5. After a successful payment, prove one ledger `PAYMENT` row exists; a replay must not add a second.
6. After a refund, prove one ledger `REFUND` row exists for that `refundId`.
7. If Docker is running, execute `PostgresCompatibilityIT` and confirm table `payments` exists.
8. Write a two-paragraph note: what would break if you copied `ddl-auto: update` into `prod`.

---

## Validation

```bash
cd reference-apps/baypay
./mvnw -pl payment-service -am test
```

Optional:

```bash
./mvnw -pl payment-service -am -Dtest=PostgresCompatibilityIT test
```

Local H2 console (profile `local` only): http://localhost:8080/h2-console JDBC URL `jdbc:h2:mem:baypay`. Inspect `PAYMENTS` and `LEDGER_TRANSACTIONS` after a curl from BUILD-301.

---

## Troubleshooting

- `Table "PAYMENTS" not found`: entity scan missed `com.baypay.shared.domain`.
- `LazyInitializationException` on GET: you added a relation and serialized it with OSIV off. Prefer ids, as the reference entities do.
- Postgres IT skipped: Docker not available — default suite can still pass; do not claim prod mapping is proven.
- Case-sensitive table names on Postgres: H2 `DATABASE_TO_LOWER=TRUE` is there for a reason; keep explicit `@Table(name = "payments")`.

---

## Expected outcome

Default tests green. You can point at the three tables and the transaction that writes them together. You have a written warning against `update` in prod.

---

## Interview questions

1. Why `@Enumerated(EnumType.STRING)` on `PaymentStatus`?
2. Why is `Money` embedded instead of two loose fields with no type?
3. What does `@Version` change under two concurrent refunds?

---

## Architecture/trade-off questions

1. Shared database for five Maven modules: when does that become the wrong default?
2. H2 for CI versus Testcontainers on every PR — cost, fidelity, flake.
3. Would you introduce Flyway in Module 3 or wait? What risk do you accept either way?

---

## Cleanup

Stop the app. If you started Postgres via Testcontainers, the JVM shutdown removes the container. Do not leave a local Docker `postgres` running unless you created it yourself — and then `docker stop` it.

---

## Cost estimate

**$0** for H2. Testcontainers uses local Docker disk/CPU only.

---

## Hidden/revealable solution

Compare mappings and profile YAML with `solutions/BUILD-303/` after your tests have run. The solution also records the ledger-count check you should have added if it was missing.

---

## What you learned

- BayPay persistence is JPA in `shared`, not a second data stack.
- H2 compatibility mode is a local tool; PostgreSQL is the prod contract.
- Transactional use cases, not controllers, own `save`.

---

## Portfolio deliverable

Include entity excerpts (`Payment` mapping + `LedgerTransaction`) and your prod `ddl-auto` paragraph with the API artifact from BUILD-301/302.
