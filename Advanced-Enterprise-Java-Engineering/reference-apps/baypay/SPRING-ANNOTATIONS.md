# Spring annotations used in BayPay

Catalog of every annotation that appears in `reference-apps/baypay` (main + test).
This is the modular monolith on **Spring Boot 3.5** / **Java 21**. BayPay is fictional.
Avery Chen is a demo customer.

**How to read the tables**

| Column | Meaning |
| --- | --- |
| Annotation | The type you see on a class, method, field, or parameter |
| Source | Who owns it. “Spring Boot” is a thin wrapper; most “Spring” work is Framework, Data, or Test |
| BayPay site | The type students should open first |
| Role | What the container or processor does |
| Teaching note | Why BayPay uses it this way |

Constructor injection is the course default. Production services do **not** put `@Autowired` on fields.

---

## 1. Bootstrap and IoC

| Annotation | Source | BayPay site | Role | Teaching note |
| --- | --- | --- | --- | --- |
| `@SpringBootApplication` | Spring Boot | `BayPayApplication` | Meta-annotation: `@Configuration` + `@EnableAutoConfiguration` + `@ComponentScan` | `scanBasePackages = "com.baypay"` is required. Default scan of `com.baypay.payment` would miss refund, worker, notification, and shared. |
| `@EntityScan` | Spring Boot | `BayPayApplication` | Registers JPA entities outside the application class package | Entities live in `com.baypay.shared.domain`. Without this, Hibernate never maps `Payment`. |
| `@EnableJpaRepositories` | Spring Data JPA | `BayPayApplication` | Creates repository proxies for `JpaRepository` interfaces | Same `com.baypay` base as the scan. `PaymentRepository` has no `@Repository` of its own. |
| `@Configuration` | Spring Framework | `BayPayConfig` | Marks a class whose `@Bean` methods populate the ApplicationContext | Use this when the type is not yours to stereotype (`Clock`) or you want an explicit test seam (`PaymentAuthorizer`). |
| `@Bean` | Spring Framework | `BayPayConfig.clock()`, `paymentAuthorizer()` | Registers the method return value as a bean | `Clock.systemUTC()` so tests can replace time. Authorizer is a `@Bean` so ITs can swap policy without touching the service. |
| `@Component` | Spring Framework | `CorrelationIdFilter`, `DemoDataSeeder`, `NotificationListener` | Generic stereotype: pick this type up in component scan | Filter, seeder, and listener are not use-cases. Do not label them `@Service`. |
| `@Service` | Spring Framework | `PaymentApplicationService`, `RefundApplicationService`, `IdempotencyService`, `PaymentPostingService`, `LeakyRefundService` | Stereotype for application/use-case beans | Same as `@Component` to the container. The name is for humans: HTTP adapters stay `@RestController`; use cases stay `@Service`. |
| `@Profile` | Spring Framework | `DemoDataSeeder` (`!prod`), `LeakyRefundService` (`leaky`) | Bean exists only when the listed Spring profile is active | Seeder must not run in `prod`. `leaky` is a teaching defect profile, never a default. |
| `@Order` | Spring Framework | `CorrelationIdFilter` (`HIGHEST_PRECEDENCE`) | Sets relative order among beans of the same kind | Correlation id must wrap the request before other filters log. |

---

## 2. HTTP adapters

| Annotation | Source | BayPay site | Role | Teaching note |
| --- | --- | --- | --- | --- |
| `@RestController` | Spring Web MVC | `PaymentController`, `RefundController` | `@Controller` + `@ResponseBody`: methods write the HTTP body (JSON) | Controllers stay thin. They map HTTP to a service call. They do not open transactions. |
| `@RequestMapping` | Spring Web MVC | Class-level `/api/v1/payments`, `/api/v1/refunds` | Shared path prefix for the controller | Version the collection in the path. Do not put verbs in the URL. |
| `@GetMapping` | Spring Web MVC | List/get payment, get refund | Maps HTTP GET | Safe and idempotent by HTTP rules. List is a query: no `Idempotency-Key`. |
| `@PostMapping` | Spring Web MVC | Create payment, create refund | Maps HTTP POST | First success **201**. Replay **200**. That status split is in the service, not in the annotation. |
| `@RequestBody` | Spring Web MVC | Create methods | Deserializes JSON to a Java record | Pair with `@Valid` or the Jakarta constraints never run. |
| `@RequestHeader` | Spring Web MVC | `Idempotency-Key` on POSTs | Binds a header to a parameter | `required = false` so a missing key becomes **400** `IDEMPOTENCY_KEY_REQUIRED` in the service, not a framework 400 you cannot document. |
| `@RequestParam` | Spring Web MVC | `GET /payments?customerId=` | Binds a query parameter | `required = false` plus `@NotNull` so missing `customerId` is **400** `VALIDATION_FAILED` via `@Validated`. |
| `@PathVariable` | Spring Web MVC | `{paymentId}`, `{refundId}` | Binds a path segment | Wrong UUID shape is **400**. Unknown id is **404** from the service. |
| `@Validated` | Spring Validation | `PaymentController` | Enables method-parameter constraints (`@NotNull` on `customerId`) | Class-level. `@Valid` alone does not validate `@RequestParam` / `@PathVariable`. |
| `@RestControllerAdvice` | Spring Web MVC | `ApiExceptionHandler` | Global `@ControllerAdvice` that writes JSON bodies | Maps domain codes to RFC 7807 `ProblemDetail`. Unknown exceptions → **500** with no stack in the body. |
| `@ExceptionHandler` | Spring Web MVC | Methods on `ApiExceptionHandler` | Handles one exception type (or a family) for that advice class | Order matters: more specific types (`IdempotencyConflictException`) before `BayPayException` and `Exception`. |

---

## 3. Jakarta Bean Validation (HTTP 400 gate)

These are not Spring types. Spring Boot runs them when `@Valid` / `@Validated` is present.

| Annotation | Source | BayPay site | Role | Teaching note |
| --- | --- | --- | --- | --- |
| `@Valid` | Jakarta Validation | Create payment/refund parameters | Cascades validation into the request record | Without this, `@NotNull` on `CreatePaymentRequest` is documentation only. |
| `@NotNull` | Jakarta Validation | Request records; list `customerId` | Rejects null | **400** `VALIDATION_FAILED`. Domain `Money` still rejects a bad amount if a caller skips HTTP. |
| `@NotBlank` | Jakarta Validation | `CreatePaymentRequest.currency` | Rejects null, empty, or whitespace | Currency is also `@Pattern`. Two gates, one field. |
| `@DecimalMin` | Jakarta Validation | `amount` on payment and refund | Minimum inclusive `0.01` | HTTP rejects zero. `Money` still forbids non-positive amounts in the domain. |
| `@Pattern` | Jakarta Validation | `currency` `USD\|EUR\|GBP` | Regex on a string | Unknown currency is **400**, not a silent USD default. |
| `@Size` | Jakarta Validation | `reference` max 64; refund `reason` max 256 | Length bound | Matches the JPA `@Column(length=…)` so HTTP fails before the SQL does. |

---

## 4. Transactions and in-process events

| Annotation | Source | BayPay site | Role | Teaching note |
| --- | --- | --- | --- | --- |
| `@Transactional` | Spring TX | `PaymentApplicationService.create`, `RefundApplicationService.create`, `IdempotencyService` writes | Starts a transaction around the method (proxy) | Self-invocation (`this.create(...)`) does **not** start a transaction. Controllers call the service so the proxy is used. |
| `@Transactional(readOnly = true)` | Spring TX | `get` / `list` on payment and refund services; idempotency lookup | Read-only hint to the session and the pool | Gets and lists must not flush a write. |
| `@EventListener` | Spring Framework | `NotificationListener` | Invokes the method when that event type is published | In-process. Same JVM as authorize. Extracting notification later means a queue and `AFTER_COMMIT`, not another `@EventListener` on a remote HTTP hop. |

---

## 5. JPA mapping (Jakarta Persistence)

Spring Data uses these. They are not Spring annotations.

| Annotation | Source | BayPay site | Role | Teaching note |
| --- | --- | --- | --- | --- |
| `@Entity` | Jakarta Persistence | `Payment`, `Refund`, `Customer`, `Account`, ledger, events, idempotency, notification | Marks a persistable type | Invariants stay on the entity / value type, not on the repository. |
| `@Table` | Jakarta Persistence | Same entities | Physical table name | `idempotency_keys`, `ledger_transactions` — names are stable for ops, not Java class names. |
| `@Id` | Jakarta Persistence | Every entity | Primary key | BayPay uses application `UUID`s, not `@GeneratedValue`. |
| `@Column` | Jakarta Persistence | Fields | Nullability, length, precision | `nullable = false` is a second line of defense after validation. |
| `@Enumerated(EnumType.STRING)` | Jakarta Persistence | `Payment.status`, `Account.status`, refund/notification enums | Store the enum **name**, not the ordinal | Ordinals break when you insert a new status in the middle. |
| `@Embedded` | Jakarta Persistence | `Payment.money`, `Refund.money`, ledger amount | Flattens an `@Embeddable` into the owner table | `Money` is a value. It is not a join to a `money` table. |
| `@Embeddable` | Jakarta Persistence | `Money` | Type that lives inside an entity | Amount `> 0`, currency `USD\|EUR\|GBP`. Embeddable does not get its own id. |
| `@AttributeOverrides` / `@AttributeOverride` | Jakarta Persistence | Money columns on payment/refund/ledger | Renames embeddable columns on that owner | Several owners embed `Money`; each maps `amount` / `currency` on its own table. |
| `@Version` | Jakarta Persistence | `Payment`, `Refund` | Optimistic lock column | Concurrent refund vs update fails closed instead of last-write-wins. |

Repositories: `*Repository extends JpaRepository<…>`. Spring Data supplies the bean. Derived methods (`findByCustomerIdOrderByCreatedAtDesc`) are the list-by-customer query. No `@Query` is used.

---

## 6. OpenAPI (springdoc)

| Annotation | Source | BayPay site | Role | Teaching note |
| --- | --- | --- | --- | --- |
| `@Tag` | Swagger / springdoc | Controllers (`Payments`, `Refunds`) | Groups operations in Swagger UI | What Harbor Market sees at `/swagger-ui.html`. |
| `@Operation` | Swagger / springdoc | Each handler | Summary on the operation | Contract text. It does not enforce idempotency; the header and service do. |

---

## 7. Tests

| Annotation | Source | BayPay site | Role | Teaching note |
| --- | --- | --- | --- | --- |
| `@SpringBootTest` | Spring Boot Test | `*ApiIT`, `*IT` | Boots the full ApplicationContext | These are slice-wider ITs, not unit tests of `Money`. |
| `@AutoConfigureMockMvc` | Spring Boot Test | HTTP ITs | Injects `MockMvc` without a real port | Same DispatcherServlet as production, no listen on 8080. |
| `@ActiveProfiles` | Spring Test | `"test"`; leaky IT uses `{"test","leaky"}` | Activates those profiles for the test context | `test` → H2 create-drop. Adding `leaky` turns on `LeakyRefundService`. |
| `@Autowired` | Spring Framework | Test classes only | Field injection of test collaborators | Allowed in tests. Forbidden as the production default (hides the graph). |
| `@MockitoSpyBean` | Spring Test | `LeakyRefundReproduceIT`, `RefundLedgerRollbackIT` | Replaces a context bean with a Mockito spy | Used to force a posting/ledger failure after HTTP 201. |
| `@ServiceConnection` | Spring Boot Testcontainers | `PostgresCompatibilityIT` | Wires the Testcontainers Postgres URL into the context | Test is `@EnabledIf("dockerAvailable")`. Default suite stays on H2. |
| `@Test` | JUnit 5 | All test methods | Marks a test | Shared module uses this without Spring. |
| `@ParameterizedTest` / `@CsvSource` | JUnit 5 | `PaymentStateMachineTest` | Runs one test per CSV row | Status transitions are data, not a wall of copy-paste. |
| `@EnabledIf` | JUnit 5 | `PostgresCompatibilityIT` | Conditionally run | Docker down → test skipped, not failed. |
| `@Override` | Java | Filters, seeder, authorizer | Compiler check for interface/class override | Not a Spring annotation. Listed so students do not confuse it with a stereotype. |

---

## 8. Intentionally unused (common in other Spring apps)

BayPay does **not** use these. Do not add them “for completeness.”

| Annotation | Why it is absent |
| --- | --- |
| Field `@Autowired` on production types | Constructor + `final` is the course default |
| `@Repository` on interfaces | Spring Data already exposes `JpaRepository` beans |
| `@Controller` (without Rest) | All HTTP is JSON |
| `@GetMapping` on writes / `@PostMapping` on reads | HTTP verb matches the use case |
| `@Async` | Notification and posting are in-process and same-transaction on purpose |
| `@Scheduled` | No settlement cron in this reference app |
| `@Cacheable` | Avery’s list is a database read, not a cache demo |
| `@GeneratedValue` | Payment ids are issued by the application |
| `@ManyToOne` / `@OneToMany` | Foreign keys are UUID columns; no JPA graph of Harbor Market objects |
| `@SpringBootApplication` without `scanBasePackages` | Would hide every module except `payment` |

---

## 9. Where the objects live

Picture: [spring-object-lifetime.svg](../../diagrams/java/baypay/spring-object-lifetime.svg) (slide PNG sibling).

The ApplicationContext keeps **one** `PaymentController` and **one** `PaymentApplicationService` proxy for the life of the process. `CreatePaymentRequest`, `Money`, and `Payment` are ordinary Java objects on the request thread. They are not beans. After `201`, the GC can collect them; the `payments` row is what remains.

## 10. Read next

1. `BayPayApplication` — why three scan annotations
2. `PaymentController` — HTTP annotations + `@Valid` / `@Validated`
3. `PaymentApplicationService` — `@Service` + `@Transactional`
4. `Payment` + `Money` — JPA vs domain rules
5. `NotificationListener` — `@EventListener` is not a second microservice
6. Lesson [L-3.1](../../course/modules/03-spring-boot-engineering/lessons/L-3.1.md) — IoC and constructor injection
