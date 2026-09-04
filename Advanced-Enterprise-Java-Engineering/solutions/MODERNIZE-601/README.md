# MODERNIZE-601 — Instructor solution

**Do not share this file with students before they submit a classification page.**

Traditional ND is the **source estate**. Liberty `server.xml` or the Spring Boot reference app is the **target**. A brief that lifts cell-scoped `jdbc/baypay` as-is, or lifts SIBus `BayPayBus` as a Liberty feature, must not outscore a disciplined TOPOLOGY-based assessment.

## What a complete artifact contains

Locked names only. Isolated target binds `jdbc/baypay-payment` and `jdbc/baypay-refund`. Management plane (`dmgr-east`, node agents) classified **drop**. Edge `ihs-east` kept. Greenfield work is Boot or Liberty — never a second `BayPayCell`.

## Expected classification

| Dependency | Type today | Primary verb | Liberty feature or replacement | Instructor notes |
|---|---|---|---|---|
| HTTP / servlet (`payment.ear`) | Web module on `PaymentCluster` | **Lift** | `servlet-6.0` + `payment-service.war` `/payment` | Same Jakarta servlet contract. Do not lift the EAR into a new cell. |
| HTTP / servlet (`refund.ear`) | Web module on `RefundCluster` | **Lift** | `servlet-6.0` + `refund-service.war` `/refund` | Wave 1 target (ARCHITECT-604). |
| EAR packaging | Cell install | **Rewrite** | WAR + `server.xml` | Thin WAR; server owns features. |
| `jdbc/baypay` | Cell-scoped DataSource, max 50 | **Rewrite** | `jdbc-4.3` + `jndi-1.0`; `jdbc/baypay-payment` and `jdbc/baypay-refund` | Shared pool is a modernization smell. `3 × 50` is a **question** until Morgan confirms per-server vs one definition. |
| `jdbc/baypayXA` | XA DataSource, not on every node | **Defer** or **drop** | none until a proven two-resource need | Incomplete bind. Local JDBC is enough for the current monolith. Do not lift XA onto every Liberty replica “for safety.” |
| `baypayDbAlias` | J2C alias | **Lift** | `server.env` / `${env.BAYPAY_DB_*}` | Secret, not XML. MODERNIZE-603. |
| `jms/paymentEvents` | Queue + connection on `BayPayBus` | **Rewrite** or **defer** | Liberty JMS / later Kafka — **not** SIBus | Equivalence is the JMS API, not the bus product. Deferring until after HTTP cutover is acceptable if named. |
| `jms/refundEvents` | Queue + connection on `BayPayBus` | **Rewrite** or **defer** | same | Wave 1 may ship HTTP refund first and leave events on ND briefly. |
| SIBus `BayPayBus` | Messaging engine in the cell | **Drop** | none | Do not recreate a bus. ME availability is the host that runs it — not HA by name. |
| `ihs-east` / `plugin-cfg.xml` | Plugin edge | **Lift** / keep | Same IHS; new plugin members for Liberty replicas | Not a WAS node. Do not drop because Liberty listens on 9080. |
| LTPA / cell SSO | Cell-wide keys | **Defer** or **drop** for `/payment` | `appSecurity` only if a portal ear remains | Not an API key. Three domains stay: merchant TLS, app authn, cell admin. |
| Cell-wide JNDI tree | DMGR-owned | **Drop** | `server.xml` per server | No cell-wide tree on the target. |
| `dmgr-east` | Management | **Drop** | none | Serving path does not include the DMGR. |
| Node agents | Management | **Drop** | none | Sync/restart story dies with ND. |
| `PaymentCluster` / `RefundCluster` as WAS clusters | ND runtime | **Rewrite** | Liberty replicas behind `ihs-east` | Density vs HA on `node-pay-2` remains a reason not to copy the cell. |
| Reporting on the payment pool | Smell | **Drop** the sharing | Own DataSource / own process | Isolated names exist so reporting cannot starve Avery Chen. |
| Sticky `JSESSIONID` on `/payment` | Plugin affinity | **Drop** | Sessionless; `Idempotency-Key` + DB | Portal ears may keep sessions on another URI group. |
| PMI / admin console | Cell ops | **Drop** | Logs / later metrics | Do not lift the console. |

Accept **defer** on XA and on JMS queues when the student names the later wave. Reject **lift** of SIBus or of cell-wide `jdbc/baypay`.

## Isolated target binds

| Target bind | Used by | Why isolated |
|---|---|---|
| `jdbc/baypay-payment` | Payment WAR / canary | Payment must not share a pool with refund or reporting |
| `jdbc/baypay-refund` | Refund WAR (Wave 1) | Refund volume must not exhaust payment connections |

## Greenfield — what you would NOT do

Do not stand up a new traditional ND cell, a new SIBus, or a cell-wide shared `jdbc/baypay` for a new BayPay service. Do not use LTPA as payment API authentication. Prefer the Spring Boot reference app or Liberty `server.xml` with isolated DataSources and `BAYPAY_DB_*`. This page exists so the cohort can operate and **leave** `BayPayCell`.

## Scoring notes

Full marks require locked names, both ears, every TOPOLOGY JNDI/messaging row, isolated target binds, SIBus dropped as a product, DMGR dropped, IHS kept, LTPA not used as API authn, and an explicit non-ND greenfield paragraph. A tidy table that lifts `jdbc/baypay` as-is caps Technical accuracy and Production awareness.
