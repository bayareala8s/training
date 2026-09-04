# ARCHITECT-401 — Instructor solution

**Do not share this file with students before they submit a brief.**

## Full mapping

| Spring (BayPay today) | Jakarta / Java EE contract | BayPay evidence | Notes |
|---|---|---|---|
| Spring IoC (`@Service`, `@Component`, `@Bean`, constructor injection) | CDI (`@ApplicationScoped`, `@RequestScoped`, `@Inject`, `@Produces`) | `PaymentApplicationService`, `BayPayConfig`, `PaymentAuthorizer` bean | Both are containers that create and inject objects. Spring’s container is not CDI unless you add a CDI adapter. |
| `@Transactional` / `PlatformTransactionManager` | JTA (`UserTransaction`, `@TransactionAttribute`, CMT) | `PaymentApplicationService.create` | Local JDBC transactions are enough for the monolith. JTA/XA is not implied. |
| `JpaRepository` | JPA `EntityManager` (`find`, `persist`, `merge`, JPQL) | `PaymentRepository`, `@Entity` types in `shared` | Spring Data is code generation over JPA. |
| `@RestController` + `@PostMapping` | JAX-RS (`@Path`, `@POST`, `Response`) | `PaymentController` | Both sit on the servlet container. |
| `application.yml` / env (`BAYPAY_DB_*`) | JNDI binds (`java:comp/env/jdbc/baypay`) | `application-prod.yml` vs historical cell resources | Same role: operator-supplied DataSource. Different binding. |
| `OncePerRequestFilter` | Servlet `Filter` | `CorrelationIdFilter` | Already Jakarta. |
| `ApplicationEventPublisher` / `PaymentCompletedEvent` | JMS (`JMSContext`) or CDI events | `PaymentPostingService` → `NotificationListener` | **Approximation.** In-process events are not crash-safe. |
| HikariCP via `spring.datasource` | Server `DataSource` + pool | Prod profile; L-4.3 keys | Same `javax.sql.DataSource`. |
| Fat JAR / `LaunchedURLClassLoader` | EAR/WAR module loaders, parent-first / parent-last | Packaging of `payment-service` vs historical ears | Isolation problem is the same. |
| No `HttpSession` on the API | `HttpSession` on legacy portal | `PaymentController` uses headers + body only | Keep it that way. |

## Transaction walk

`create()` is `@Transactional`. `PaymentPostingService.postAuthorized` has **no** annotation, so it joins the caller (`REQUIRED` / default). Payment row, idempotency, audit, and ledger commit together. Jakarta equivalent: `@TransactionAttribute(REQUIRED)` on both, or only on the facade.

A `REQUIRES_NEW` on posting is the INCIDENT-403 class of mistake.

## Greenfield vs source estate

Operators used to bind `jdbc/baypay` and `jms/paymentEvents` in a WAS cell. Boot binds the JDBC URL through env and YAML. **Do not** create a new traditional ND cell for a new BayPay service. Prefer Spring Boot (this reference app) or Liberty with `server.xml` when an ear must remain an ear. Module 5 documents ND so students can operate and leave it.

## Scoring notes

Full marks require BayPay evidence on the five required rows, at least one extra honest approximation (events ≠ JMS), the join-caller observation, and an explicit non-WAS greenfield sentence.
