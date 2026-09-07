# INTERVIEW-1602 rapid-fire log

**Command:** `python3 interview-bank/simulator.py --mode rapid-fire --count 10 --seed 16`  
**Reveal:** after all ten. `solutions/INTERVIEW-1602/` not opened first.  
**Payment named:** Avery / `c1602b22-0000-4000-8000-111111111602` on IQ-001.  
**No portal / Bedrock / AWS apply.**

| # | Id | Domain | Sec | Score |
|---|---|---|---|---|
| 1 | AEJE-IQ-047 | Containers/K8s | ~75 | ok |
| 2 | AEJE-IQ-061 | AWS | ~70 | ok |
| 3 | AEJE-IQ-062 | AWS | ~70 | ok |
| 4 | AEJE-IQ-037 | WebSphere/Liberty | ~80 | ok |
| 5 | AEJE-IQ-054 | Containers/K8s | ~80 | thin |
| 6 | AEJE-IQ-030 | Spring/Jakarta | ~85 | ok |
| 7 | AEJE-IQ-058 | Containers/K8s | ~75 | ok |
| 8 | AEJE-IQ-001 | Java/JVM | ~90 | ok |
| 9 | AEJE-IQ-053 | Containers/K8s | ~70 | ok |
| 10 | AEJE-IQ-085 | Linux/TLS | ~80 | ok |

---

## 1. AEJE-IQ-047 — read-only root

Sam wants a read-only root for `payment-service`. Java 21 Boot still needs a **writable `/tmp`** (and usually a log/scratch dir — Tomcat/Hibernate work). I refuse a writable **fat JAR**, writable `/`, and **`--privileged`**. Put tmp on an emptyDir; logs to stdout or a mounted volume. I will not leave the image layer writable “so Hibernate can compile.”

**Refuse:** privileged, write-the-JAR-at-runtime.

## 2. AEJE-IQ-061 — ECR scan-on-push

Block the payment image on **critical/high in the JRE/runtime** that we actually ship. Ticket **low** findings and **test-only** layers. `:latest` plus “rescan tomorrow” is not a control — pin a digest/tag, IMMUTABLE repo. I will not stop the train for a CVE that never reaches the Fargate task.

**Refuse:** `:latest` as the promotion tag.

## 3. AEJE-IQ-062 — execution vs task role

**Execution** role: pull image, logs, inject `BAYPAY_DB_*` (`GetSecretValue` + `kms:Decrypt` on `alias/baypay-payments`). **Task** role: what the JVM assumes. If the app only talks JDBC, task role is **near-empty**. Copying execution onto the task means a stolen JVM can pull secrets. I will not attach `AdministratorAccess`.

**Refuse:** task = execution “to be safe.”

## 4. AEJE-IQ-037 — pool vs DB busy

Pool exhaustion: `jdbc/baypay` **50/50**, waiters, threads parked on getConnection. DB saturation: writer CPU/`max_connections` high, waits **inside** Postgres. First: PMI + which replica — do **not** bounce `db-east` or raise `maxConnections` blindly (you can knock over the writer). Harbor Market slow POST is not “Morgan said busy.”

**Refuse:** raise maxConnections as step one.

## 5. AEJE-IQ-054 — golden Helm vs team charts

Golden path owns **probes, heap-vs-limit (no `-Xmx` = cgroup), secrets, non-root**. Team charts if they must, with an **expiry** and a diff against golden. I will not let Riley fork probes so canary skips readiness. Trade-off / decide later in 1604: how many exceptions.

**Refuse:** unbounded team chart as the forever path. *(thin — clock)*

## 6. AEJE-IQ-030 — Spring ↔ Jakarta

`@Service` + ctor inject ≈ `@ApplicationScoped` / `@Inject`. `@Transactional` ≈ JTA / container tx; `UserTransaction` is the **bean-managed** escape. Validation/JPA names move; persistence is still a unit. I would **not** rewrite Morgan’s Liberty module to Boot on day one — read it, map it, ship Harbor Market.

**Refuse:** “rewrite Liberty first.”

## 7. AEJE-IQ-058 — canary wrong Pods

Compare **Deployment labels, Pod labels, Service selector**. Endpoints empty or pointing at the canary = selector miss (class, not a hallway RCA). Stabilize: fix selector / a second Service — **do not delete** the prod Service. I will not “kubectl delete svc” to clear the canary.

**Refuse:** delete the production Service.

## 8. AEJE-IQ-001 — JMM `posted` flag

Plain `boolean posted` has **no happens-before** — thread B can still see `false` after A’s ledger insert, so Avery’s `$84` / `c1602b22-…1602` can post twice. I want **`volatile`**, a **lock**, or (better) **don’t use a heap flag** — idempotency row + unique payment id. A DB unique constraint is **not** a JVM visibility fix; both can be true.

**Refuse:** “the unique key solved the race.”

## 9. AEJE-IQ-053 — CI RBAC

Pipeline SA: **Role** in `baypay-prod` only (deploy/roll). No **cluster-admin**, no `*` on secrets cluster-wide. ClusterRole only if you must, bound to that SA + namespace. I will not grant the deploy robot the cell.

**Refuse:** `cluster-admin` on the deploy robot.

## 10. AEJE-IQ-085 — `ss` + thread dump

Read them **together**. ESTABLISHED + many **BLOCKED** servlet threads ≠ “network down.” CLOSE_WAIT + **RUNNABLE** workers is a different story. Hikari waiters show as threads in `getConnection` **and** as pending on the pool metric — not as a Postgres bounce. I will not bounce `dmgr-east` from a dump.

**Refuse:** one artifact as the whole RCA.

---

## Reveal gaps (after the set)

- IQ-047: bank may want Hibernate *and* Tomcat scratch named separately — I said `/tmp` + emptyDir.
- IQ-054: thinnest; missed a concrete expiry example.
- IQ-001: could have named `synchronized` release as a happens-before edge more crisply.
- Did not paste bank text into the spoken log.
