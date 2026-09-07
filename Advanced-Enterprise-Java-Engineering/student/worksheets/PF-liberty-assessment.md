# Portfolio — Liberty migration assessment (inventory)

**Course:** Advanced Enterprise Java Engineering  
**Module:** 06  
**Lab:** MODERNIZE-601  
**Case study:** BayPay Financial Services (fictional)

Export this page (or a copy) as the assessment half of the Module 6 portfolio artifact. Pair it with [PF-liberty-waves.md](PF-liberty-waves.md) from ARCHITECT-604. Use locked names from [datasets/baypay-cell/TOPOLOGY.md](../../datasets/baypay-cell/TOPOLOGY.md) only. Traditional ND is the **source estate**. Liberty or Spring Boot is the **target**.

**Your name:**  
**Date:** 2026-09-06  
**Cohort / reviewer (if any):**  

---

## 1. Source applications

| Ear | Cluster | Members | Context | What you will package on Liberty |
|---|---|---|---|---|
| `payment.ear` | `PaymentCluster` | `Pay1` (`node-pay-1`), `Pay2` + `Pay3` (`node-pay-2`) | `/payment` | `payment-service.war` (or keep the Boot fat JAR as the teaching runtime). Not a second EAR cell. |
| `refund.ear` | `RefundCluster` | `Ref1`, `Ref2` (both `node-ref-1`) | `/refund` | `refund-service.war` (Wave 1 target — lower volume). Same rule: WAR + `server.xml`, not `refund.ear` on a new ND cluster. |

No fourth payment member. `ihs-east` is the edge, not a cluster member.

---

## 2. Dependency classification

Use exactly one primary verb per row: **lift** / **rewrite** / **defer** / **drop**. Name a Liberty feature (`servlet-6.0`, `jdbc-4.3`, `jndi-1.0`, `persistence-3.1`) or isolated bind, or `none`.

| Dependency | Type today | Scope today | Lift / rewrite / defer / drop | Liberty feature or replacement | Notes |
|---|---|---|---|---|---|
| HTTP / servlet (`payment.ear`) | Servlet / web module | `PaymentCluster` `/payment` | **lift** | `servlet-6.0` | Lift the contract, not the EAR. Package `payment-service.war`. |
| HTTP / servlet (`refund.ear`) | Servlet / web module | `RefundCluster` `/refund` | **lift** | `servlet-6.0` | Same: `refund-service.war`. Wave 1 HTTP cutover. |
| EAR packaging | `payment.ear` / `refund.ear` | Cell application target | **rewrite** | WAR + `webApplication` in `server.xml` | An EAR is a cell-deployable bundle. Liberty is a per-process drop-in, not a smaller cell. |
| `jdbc/baypay` | DataSource | **Cell-scoped** (historical share) | **rewrite** | `jdbc-4.3` + `jndi-1.0` + isolated `jdbc/baypay-payment` / `jdbc/baypay-refund` | Not a clean lift of the same name. INC-WAS-503: `reporting.ear` on Pay1 starved `payment.ear` because both looked up cell `jdbc/baypay`. |
| `jdbc/baypayXA` | XA DataSource | Incomplete — not on every node (INC-WAS-504) | **defer** | none this wave | 4.12 required it; it was never created. Do not lift XA onto every Liberty replica. Local `jdbc-4.3` is enough until a named two-phase story exists. |
| `baypayDbAlias` | J2C auth alias | Cell (username/password for the DS) | **lift** | `server.env` / `${env.BAYPAY_DB_*}` | Lift the **secret**, not the alias object. Never commit credentials in `server.xml`. |
| `jms/paymentEvents` | Queue + QCF | SIBus `BayPayBus` | **rewrite** | JMS API later, or in-process / Boot events now | Equivalence is the JMS API, not the bus. Defer the queue until after Wave 2 if HTTP cutover cannot wait — accepted risk: payment/refund lose async fan-out until a replacement lands. |
| `jms/refundEvents` | Queue + QCF | SIBus `BayPayBus` | **defer** | none in Wave 1 HTTP | Wave 1 moves `/refund` HTTP. Queue stays on `RefundCluster` / `BayPayBus` until a named rewrite (JMS on Liberty, Kafka, or in-process). Dual-run risk: Liberty refund HTTP vs ND refund listener. |
| SIBus `BayPayBus` | Messaging engine | Cell bus | **drop** | none | Product, not a Liberty feature. Do not recreate a messaging engine and call it done. Capability moves with the queue rows (rewrite/defer). No new traditional bus for greenfield. |
| `ihs-east` / `plugin-cfg.xml` | HTTP edge / plugin | `ihs-east.baypay.example` | **lift** | keep the edge (IHS or equivalent LB) | Not a WAS node. Do not drop because Liberty listens on 9080. Merchants already trust this path (INC-WAS-502). |
| LTPA / cell SSO | Cell LTPA keys | `BayPayCell` browser/portal SSO | **drop** | none for `/payment` | Not an API key for Avery Chen. Payment authn is Idempotency-Key + app identity, not cell SSO. Defer only if a leftover portal ear still needs it on ND. |
| Cell-wide JNDI tree | Naming | `BayPayCell` | **drop** | `jndi-1.0` **per process** | Target has no cell-wide tree. INC-WAS-504: 4.12 resource-ref ≠ DataSource object. Binds live in `server.xml`. |
| `dmgr-east` | Deployment manager | `was-dmgr-east.baypay.example` | **drop** | none | Control plane, not a serving feature. Avery can 201 while Priya cannot open the console. |
| Node agents | `nodeagent-pay-1/2`, `nodeagent-ref-1` | on `node-pay-*` / `node-ref-1` | **drop** | none | Sync/start/stop of ND members. INC-WAS-504: agent bounce ≠ member down, but it **does** break distribute. Liberty has no node agent. |
| Shared pool / reporting | Nightly jobs vs payment pool | Historically `jdbc/baypay` | **rewrite** | dedicated reporting DS / batch host | Reporting must not share the payment pool on the target (INC-WAS-503 / INC-EE-402). |
| Sticky `JSESSIONID` on `/payment` | Plugin affinity | IHS → member | **drop** | none | `/payment` is idempotent HTTP, not a portal session. Do not lift WAS sticky as a Liberty session feature. |

Optional extras (locked names only):

| Dependency | Type today | Scope today | Lift / rewrite / defer / drop | Liberty feature or replacement | Notes |
|---|---|---|---|---|---|
| Admin console / `dmgr-east` UI | Management | Cell | **drop** | none | Literacy until cutover. Not a Liberty feature. |
| PMI / `jdbc/baypay` PercentUsed | Ops telemetry | Per member (not `3 × 50`) | **rewrite** | Micrometer / Liberty monitor + alerts on waiters | Same gauge story as Hikari (INC-EE-402). Per-process, not cell PMI. |
| WAS parent-last class loaders | Packaging habit | Ear / WAR | **drop** | none | Do not lift loader tricks. Jakarta namespace on the WAR; Boot 3.5.5 already `jakarta`. |

---

## 3. Isolated target binds

Write the two DataSource JNDI names you will use on Liberty and why you will **not** keep `jdbc/baypay` as a cell-wide (or server-wide shared) name.

| Target bind | Used by | Why isolated |
|---|---|---|
| `jdbc/baypay-payment` | Payment WAR | Payment checkout cannot share a max with refund or reporting. Same JVM or same `server.xml` name would recreate INC-WAS-503 (`reporting.ear` + `payment.ear` both on cell `jdbc/baypay`, Pay1 50/50). |
| `jdbc/baypay-refund` | Refund WAR | Refunds are Wave 1 and lower volume. A hung settlement preview must not take refund (or payment) connections. Separate pool, separate `server.env` if the processes split. |

Keeping one `jdbc/baypay` on Liberty — even “just this server” — is still a shared name. The next job that looks it up wins. Isolated names make the steal visible at bind time.

Is `3 × 50` a fact or a question until Morgan Hale confirms DataSource scope?

**A question.** WAS `maxConnections = 50` in incidents is **per member** (Pay1 50/50 while Pay2 was 11). Postgres `max_connections` is a different ceiling. `3 × 50` is only true if Morgan confirms each of Pay1/Pay2/Pay3 has its own pool of 50 **and** you are counting JVM pools, not one cell object and not one Postgres limit. Until that confirm, treat 50 as “this JVM’s pool,” not “the database is 150.”

---

## 4. What you would NOT do for greenfield

A new BayPay service (for example an FX quote API) is requested tomorrow. In 6–10 sentences, state what you would **not** copy from `BayPayCell` (new DMGR, cell-wide `jdbc/baypay`, new SIBus, LTPA as API authn) and what you would use instead (Liberty `server.xml` with isolated DataSources, and/or the Spring Boot reference app). This paragraph is required.

I would **not** stand up a second traditional ND cell, a new `dmgr-east`, or new node agents. “We already have a cell” is inventory, not a design. I would **not** bind a cell-wide (or server-wide) `jdbc/baypay` for the FX API — not even if Morgan offers the name this afternoon — because INC-WAS-503 showed a new ear on that name can starve payment. I would **not** create a new SIBus or messaging engine; `BayPayBus` is a product we are dropping, and “we already have SIBus” is a weak reason to keep it after `refund.ear` leaves `RefundCluster`. I would **not** use cell LTPA keys as how the FX API authenticates callers. Instead I would ship either a Liberty `server.xml` (`servlet-6.0`, `jdbc-4.3`, `jndi-1.0`, `persistence-3.1`) with an isolated DataSource (`jdbc/baypay-fx` or similar) and secrets in `server.env` (`BAYPAY_DB_*`), or — preferred for a blank-page service — the Spring Boot 3.5.5 / Java 21 reference shape (`reference-apps/baypay`) with Hikari and YAML. Edge stays `ihs-east` or an equivalent load balancer; Liberty-on-9080 is not a replacement for the merchant path. Traditional ND remains how we operate `payment.ear` until waves 1–3; it is not the shape of the next service.

---

## 5. Interview snippet (Staff, 6–8 sentences)

Explain to Morgan Hale, Jordan Voss, and a Spring engineer, in one sitting, why lifting `servlet-6.0` is not the same as lifting the cell, and why this page is an inventory of an estate you intend to leave.

`servlet-6.0` means the container still runs HTTP servlets — `payment-service.war` / `refund-service.war` — so Avery can POST `/payment` without a Boot rewrite this quarter. That is a **contract**. The cell is a **habit**: `dmgr-east`, node agents, cell-scoped `jdbc/baypay`, SIBus `BayPayBus`, LTPA, and an EAR targeted at `PaymentCluster`. Liberty enables the contract in `featureManager` and binds isolated names in `server.xml`; it does not give you a smaller DMGR. Jordan’s 4.12 window (INC-WAS-504) already showed a green cell checkbox is not “every member has the bits,” and Morgan’s shared pool (INC-WAS-503) already showed a cell JNDI name is a stealable resource. This page lists those dependencies so we can lift, rewrite, defer, or drop them on purpose. We keep operating `BayPayCell` until Wave 3. We do not copy it. The Spring engineer should hear: Boot stays the teaching and greenfield runtime; Liberty is the ear-compatible exit when the war cannot rewrite yet — both beat a second Deployment Manager.
