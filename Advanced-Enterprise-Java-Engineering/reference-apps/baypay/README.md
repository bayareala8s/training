# BayPay Enterprise Payment Platform

Fictional reference application for **BayLearn — Advanced Enterprise Java Engineering**.

BayPay is a **modular monolith**: one deployable Spring Boot process, five Maven modules that can be extracted later. That is a deliberate architecture choice, not a missing microservice step.

## When a modular monolith is preferable

Prefer this shape when:

- One team owns the payment lifecycle
- You need a single transaction across authorize → ledger post → notify
- You do not yet have independent scale, failure, or release SLAs per module
- Idempotency and audit are easier to guarantee in one database

Extract a module to a network service when it has a different scale profile, a different data store, or a team that must release independently. Do not extract `notification-service` or `transaction-worker` just to draw more boxes.

```text
Customers → payment-service (composition root)
              ├── refund-service
              ├── transaction-worker   (in-process event)
              └── notification-service (in-process event)
                    └── shared (domain + JPA)
```

## How to read the source

Javadoc on types is written for students. Start in this order:

1. `shared/.../domain/package-info.java` — value vs entity, where invariants live
2. `Money`, `Payment`, `PaymentStatus`, `PaymentStateMachine` — Module 1
3. `PaymentAuthorizer` then `PaymentApplicationService` — SOLID seams and orchestration
4. `PaymentPostingService` then `NotificationListener` — why posting and email are not on `Payment`
5. `IdempotencyService` — replay vs 409

Comments explain *why* (fail closed, happens-before, no `setStatus`). They do not narrate getters.

## Modules

| Module | Role |
|---|---|
| `shared` | Customer, Account, Payment, Refund, ledger Transaction, TransactionEvent, AuditEvent, state machine, idempotency |
| `payment-service` | REST API + runnable application |
| `refund-service` | Refund use cases |
| `notification-service` | Email/webhook records on completion events |
| `transaction-worker` | Posts authorized payments to the ledger |

## Payment state

`RECEIVED → VALIDATING → AUTHORIZED → PROCESSING → COMPLETED`

Failure / reversal: `DECLINED`, `FAILED`, `REVERSED`.

Idempotency is required on `POST /api/v1/payments` and `POST /api/v1/refunds`. Replaying the same `Idempotency-Key` and body returns the original resource. A different body with the same key returns `409`.

## Run locally

Java 21. Maven Wrapper is included.

```bash
export JAVA_HOME="$(/usr/libexec/java_home -v 21 2>/dev/null || echo /opt/homebrew/opt/openjdk@21)"
./mvnw -pl payment-service -am test
./mvnw -pl payment-service -am spring-boot:run
```

- API: http://localhost:8080
- OpenAPI: http://localhost:8080/swagger-ui.html
- Health: http://localhost:8080/actuator/health
- H2 console (local profile): http://localhost:8080/h2-console

Demo customer (fictional):

| Field | Value |
|---|---|
| customerId | `11111111-1111-1111-1111-111111111111` |
| active account | `22222222-2222-2222-2222-222222222221` |
| frozen account | `22222222-2222-2222-2222-222222222222` |

```bash
curl -sS -X POST http://localhost:8080/api/v1/payments \
  -H 'content-type: application/json' \
  -H 'Idempotency-Key: demo-pay-001' \
  -H 'X-Correlation-Id: local-1' \
  -d '{
    "customerId":"11111111-1111-1111-1111-111111111111",
    "accountId":"22222222-2222-2222-2222-222222222221",
    "amount":25.00,
    "currency":"USD",
    "reference":"invoice-1001"
  }'
```

## Profiles

| Profile | Database |
|---|---|
| `local` (default) | H2 in-memory, PostgreSQL compatibility mode |
| `test` | H2 create-drop |
| `prod` | PostgreSQL via `BAYPAY_DB_URL`, `BAYPAY_DB_USER`, `BAYPAY_DB_PASSWORD` |

Testcontainers PostgreSQL is on the classpath. `PostgresCompatibilityIT` runs only when Docker is available.

## What this is not

- Not a real bank, card network, or employer system
- Not a service mesh
- Not production PCI scope — secrets and network controls are taught in later modules
