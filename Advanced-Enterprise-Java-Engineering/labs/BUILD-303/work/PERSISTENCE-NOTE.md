# BUILD-303 — Persistence note

Date: 2026-09-06

## What is stored

| Table | Mapping | Notes |
|---|---|---|
| `payments` | `Payment` | unique `idempotency_key`, `@Enumerated(STRING)` status, embedded `Money`, `@Version` |
| `refunds` | `Refund` | unique key, `findByPaymentIdAndStatus`, `@Version` |
| `ledger_transactions` | `LedgerTransaction` | type `PAYMENT` / `REFUND`; refund rows also store `refund_id` |

`Money` is `@Embeddable` (`amount` scale 2, `currency` length 3). Entities hold ids, not lazy graphs — `open-in-view: false` on local, test, and prod. `@EntityScan` / `@EnableJpaRepositories` / component scan are `com.baypay`. Services own `@Transactional`, not controllers.

Profiles: local H2 `ddl-auto: update` (`MODE=PostgreSQL`, `DATABASE_TO_LOWER=TRUE`); test H2 `create-drop`; prod PostgreSQL `validate`.

## Ledger proof

`LedgerPersistenceIT`: first `$40` create → one `PAYMENT` row; identical replay → still one; `$15` refund → one `REFUND` row for that `refundId`.

## What breaks if you copy `ddl-auto: update` into prod

Hibernate would treat the live schema as something it may alter on boot: add columns, widen types, invent tables. That is convenient on a throwaway H2 mem database. In prod it is an unreviewed migration. A renamed field or a new `NOT NULL` without a default can lock `payments` during a rolling deploy, or rewrite a type (`STRING` enum vs ordinal leftover) and silently map `COMPLETED` to the wrong ordinal after a restart.

`validate` fails fast when the schema and entities disagree. Schema change then belongs in an explicit migration (Flyway later), reviewed, and applied once. Module 3 accepts “H2 updates itself; Postgres is validated” — the risk is that a mapping that only ever ran on H2 `update` can still fail `validate` on Postgres (reserved words, case, types). That is why `PostgresCompatibilityIT` exists when Docker is up, and why table names are explicit (`payments`, not a quoted mixed-case surprise).

## Interview

- **STRING enums:** ordinal `0/1/2` breaks when you insert `REVERSED` in the middle of the enum. The column stores `COMPLETED`.
- **Embedded Money:** one type, one constructor, one scale rule. Two loose columns let a caller write `amount=10.001` and `currency=usd`.
- **`@Version`:** two concurrent refunds that also `transitionTo(REVERSED)` on the same payment: the second flush hits `OptimisticLockException` instead of a silent last-write-wins on status.
