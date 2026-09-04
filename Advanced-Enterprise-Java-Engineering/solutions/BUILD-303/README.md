# Solution — BUILD-303 Persistence

Instructor only.

## Target mappings

| Type | Table | Notes |
|---|---|---|
| `Payment` | `payments` | Embedded `Money`, STRING status, unique `idempotencyKey`, `@Version` |
| `Refund` | `refunds` | Same money mapping, `findByPaymentIdAndStatus` |
| `LedgerTransaction` | `ledger_transactions` | Type `PAYMENT` / `REFUND`, optional `refundId` |
| `IdempotencyRecord` | (idempotency store) | Operation + key uniqueness used by writes |

Entities: `reference-apps/baypay/shared/src/main/java/com/baypay/shared/domain/`.  
Repositories: `.../persistence/`.  
Scan: `@EntityScan` + `@EnableJpaRepositories` on `com.baypay` in `BayPayApplication`.

## Profiles

| Profile | URL | `ddl-auto` | Console |
|---|---|---|---|
| `local` | H2 mem `baypay` `MODE=PostgreSQL` | `update` | on |
| `test` | H2 mem `baypaytest` | `create-drop` | off |
| `prod` | `BAYPAY_DB_*` PostgreSQL | `validate` | off |

`open-in-view: false` in local and prod.

## Atomic write (what students must prove)

`PaymentApplicationService.create` is `@Transactional`. `PaymentPostingService.postAuthorized` joins that transaction. After `201`, one `ledger_transactions` row of type `PAYMENT`. After replay `200`, still one.

Refund create is the same pattern for type `REFUND`.

## Postgres check

`PostgresCompatibilityIT` uses Testcontainers `postgres:16-alpine` and `@ServiceConnection` when Docker is available. It asserts `information_schema.tables` contains `payments`. Skipping it without Docker is allowed; claiming “prod ready” without it is not.

## Prod `ddl-auto` paragraph (expected student argument)

`update` in production lets Hibernate emit DDL at boot under traffic. That can add columns, widen types, or fail halfway. `validate` fails closed when mappings and PostgreSQL disagree, which is the operational contract. Schema change belongs in a migration tool (later), not in entity auto-update.

## Validation command

```bash
cd reference-apps/baypay
./mvnw -pl payment-service -am test
```

## Rubric notes

Technical accuracy: mappings + finders + one-ledger-row proof. Production awareness: profile table and `validate`. Trade-offs: H2 versus Testcontainers.
