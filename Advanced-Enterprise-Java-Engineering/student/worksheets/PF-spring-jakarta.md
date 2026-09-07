# Portfolio — Spring-to-Jakarta mapping brief

**Course:** Advanced Enterprise Java Engineering  
**Module:** 04  
**Lab:** ARCHITECT-401  
**Case study:** BayPay Financial Services (fictional)

Export this page (or a copy) as your Module 4 portfolio artifact.

**Your name:**  
**Date:** 2026-09-06  
**Reference app commit / tag (if known):** local Downloads workspace (`reference-apps/baypay`)

---

## Required mapping

| Spring (BayPay today) | Jakarta contract | Evidence (type or file) | Notes |
|---|---|---|---|
| IoC (`@Service`, constructor injection) | CDI (`@ApplicationScoped`, `@Inject`) | `PaymentApplicationService`, `PaymentController`, `BayPayConfig` (`Clock`, `PaymentAuthorizer` beans) | The container constructs the graph. Tests replace `PaymentAuthorizer`. Same idea as a CDI bean; Boot’s factory is Spring, not Weld. |
| `@Transactional` | JTA (`UserTransaction`, `@TransactionAttribute(REQUIRED)`) | `PaymentApplicationService.create`, `RefundApplicationService.create` | One unit of work: payment + ledger + idempotency. Spring TM talks JPA; it is not a different transaction model. Default rollback is runtime exceptions (FIX-304). |
| `JpaRepository` | JPA `EntityManager` | `PaymentRepository`, `@Entity Payment` / `Refund` / `LedgerTransaction` on `payments`, `refunds`, `ledger_transactions` | Repositories are typed facades. Entities and `@Embedded Money` are the JPA mapping. `@EntityScan("com.baypay")`. |
| `@RestController` | JAX-RS (`@Path`, `@POST`) | `PaymentController`, `RefundController` | HTTP verbs and JSON on a servlet. BayPay picked MVC because the Boot stack and OpenAPI starter are already wired — not because JAX-RS cannot express POST. |
| `application.yml` / `BAYPAY_DB_*` | JNDI resource binds | `application-prod.yml` (`BAYPAY_DB_URL` / user / password) vs historical `jdbc/baypay` | Same `javax.sql.DataSource`. Operators used to bind the name in the cell; Boot binds URL and pool in YAML / env. |

## Extra rows (at least three)

| Spring / Boot | Jakarta / server | Evidence | Notes |
|---|---|---|---|
| `OncePerRequestFilter` | Servlet `Filter` | `CorrelationIdFilter` | Runs on the request thread before the controller. Echoes `X-Correlation-Id`. Health can still be UP while workers hang (INCIDENT-202). |
| `ApplicationEventPublisher` | CDI events or JMS (approximation) | `PaymentCompletedEvent` → `NotificationListener` `@EventListener` | In-process and still inside the payment transaction. Not crash-safe. A later queue is JMS / Kafka, not this listener. |
| Hikari via `spring.datasource` | Server `DataSource` + pool | `application-local.yml` H2; prod Postgres URL; Boot Hikari defaults | Same JDBC contract. Exhaustion is waiters and `active == max`, not “JPA is slow.” |
| Fat JAR / embedded Tomcat | EAR / WAR + server class loaders | `payment-service` `spring-boot:run` | One JVM, Maven modules on one classpath. An EAR on PaymentCluster is parent-first / shared libs — Module 5 source estate, not a new cell. |

## Transaction walk

Does `PaymentPostingService.postAuthorized` start its own transaction in the **reference app**? What Jakarta attribute matches that?

No. `postAuthorized` has **no** `@Transactional`. `create()` is `@Transactional` and calls posting on the same thread. The ledger `PAYMENT` row, payment `COMPLETED`, and idempotency remember **join** that transaction. Jakarta: `create` is `@TransactionAttribute(REQUIRED)`. Posting must **not** be `REQUIRES_NEW` today — a second transaction could commit the ledger after `create` rolls back (or the reverse). FIX-304 is the refund twin: do not catch and commit half the work. Extraction later is an outbox in this same commit, then a worker, not `REQUIRES_NEW` on the HTTP thread.

## Greenfield vs source estate

On the historical cell, operators bound `jdbc/baypay` (and typically a JMS name for payment events) in the cell-wide JNDI tree; the EAR looked up the name. Boot binds the same DataSource with `BAYPAY_DB_URL` / user / password in `application-prod.yml` and lets Hikari own the pool.

I would **not** create a new traditional WAS ND cell for a new BayPay service: ND is the estate we migrate off (dmgr, cluster, IHS), not a blank-page runtime. Greenfield is this Boot monolith or Liberty with externalized config.

## Interview snippet (Staff, 6–8 sentences)

BayPay’s payment API is already a Jakarta application. `PaymentController` is a servlet resource, `CorrelationIdFilter` is a `Filter`, `Payment` is a JPA entity, and `@Transactional` is the JTA unit of work that includes `PaymentPostingService`. Spring names are the facades we type; the contracts are Servlet, JPA, JTA, and `DataSource`. That is why a WAS operator and a Spring engineer can share one picture: Avery’s `$25` POST still needs one commit for payment plus ledger. It does not follow that the next service should be an EAR on PaymentCluster. Traditional ND is literacy and a source topology — cell-wide JNDI and parent-first loaders are what we are leaving. A new service should be Boot or Liberty with config in the environment, the unique `idempotency_key` in Postgres, and posting still in one transaction until we add an outbox on purpose.
