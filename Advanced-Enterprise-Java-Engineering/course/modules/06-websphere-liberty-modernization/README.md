# Module 6 — WebSphere Liberty Modernization

**Duration:** ~2.5 hours of lessons plus 4 labs  
**Case study:** BayPay Financial Services (fictional)  
**Theme:** Move BayPay from traditional WAS ND toward Liberty  
**Portfolio artifact:** Liberty migration assessment from [MODERNIZE-601](../../../labs/MODERNIZE-601/README.md) and [student/worksheets/PF-liberty-assessment.md](../../../student/worksheets/PF-liberty-assessment.md)

BayPay is a fictional payments company used throughout this course. It is not a real bank, card network, IBM customer, or employer. Every customer, account, hostname, dump, and metric you see is synthetic.

**Delivery note:** this module is **simulation plus configuration files on disk**. A licensed WebSphere ND cell is **not** required. A live Liberty or Open Liberty server is **not** required. You will assess ears on paper, write `server.xml` / `server.env`, and design waves. Optional Open Liberty on a laptop is fine if you want to validate XML locally; it is not a graded dependency.

---

## Business context

BayPay’s **source estate** is still the traditional WebSphere Network Deployment cell `BayPayCell` from Module 5. Merchants hit `payment.ear` on `PaymentCluster` (`Pay1`, `Pay2`, `Pay3`) and `refund.ear` on `RefundCluster` (`Ref1`, `Ref2`). IBM HTTP Server `ihs-east` terminates TLS. Cell-scoped `jdbc/baypay` and SIBus `BayPayBus` are the bindings those ears grew up with.

That cell is what you **leave**. This module moves BayPay **toward Liberty**: one process, `server.xml` on disk, features you enable by name, and **isolated** DataSources `jdbc/baypay-payment` and `jdbc/baypay-refund`. Do not keep one cell-wide pool. Do not recommend a new traditional ND cell for a blank-page service.

The **teaching application** remains `reference-apps/baypay` (Spring Boot 3.5.5, Java 21). Liberty is the **ear-compatible path** when `payment.ear` / `refund.ear` must stay Jakarta wars this quarter instead of a full Boot rewrite. Greenfield modules still start on Boot. Both targets beat a second Deployment Manager.

The locked inventory lives in [datasets/baypay-cell/TOPOLOGY.md](../../../datasets/baypay-cell/TOPOLOGY.md). Reuse those names in every diagram, lab, and interview answer:

| Role | Locked name |
|---|---|
| Cell (source) | `BayPayCell` |
| Payment cluster | `PaymentCluster` members `Pay1`, `Pay2`, `Pay3` |
| Refund cluster | `RefundCluster` members `Ref1`, `Ref2` |
| Source applications | `payment.ear` (`/payment`), `refund.ear` (`/refund`) |
| Source DataSource | `jdbc/baypay` (cell-scoped historically) |
| Liberty DataSources | `jdbc/baypay-payment`, `jdbc/baypay-refund` |
| Liberty packaging | `payment-service.war`, `refund-service.war` |
| Messaging (source) | SIBus `BayPayBus`, `jms/paymentEvents`, `jms/refundEvents` |
| Edge | `ihs-east` / `ihs-east.baypay.example` |
| Features students write | `servlet-6.0`, `jdbc-4.3`, `jndi-1.0`, `persistence-3.1` |

Demo identities remain:

| Role | Synthetic id |
|---|---|
| Customer Avery Chen | `11111111-1111-1111-1111-111111111111` |
| Active USD account | `22222222-2222-2222-2222-222222222221` |
| Frozen USD account | `22222222-2222-2222-2222-222222222222` |

On-call names used in production examples: **Priya Nair** (SRE), **Riley Okonkwo** (application on-call), **Morgan Hale** (WAS cell administrator), **Jordan Voss** (release engineer).

Migration waves (ARCHITECT-604) are locked: **0** inventory, **1** refund on Liberty, **2** payment canary, **3** decommission ND after an SLO hold.

---

## Learning objectives

After this module you can:

- Contrast traditional WAS ND (`BayPayCell`, DMGR, node agents, cell JNDI) with Liberty (`server.xml`, features, per-process config) and say why Boot remains the teaching runtime.
- Write a Liberty `server.xml` that enables `servlet-6.0`, `jdbc-4.3`, `jndi-1.0`, and `persistence-3.1`, binds isolated DataSources, and deploys `payment-service.war` / `refund-service.war`.
- Assess what can move from an ear (servlets, JDBC lookups after rename) and what cannot lift-and-shift (SIBus, cell-wide JNDI, WS-* proprietary bindings, `javax` vs `jakarta`, WAS class-loader tricks).
- Externalize config with `server.env` and variables so `BAYPAY_DB_*` secrets never live in committed XML.
- Design waves 0–3 with canary and dual-run, and write rollback for refund then payment without standing up a live cell.

---

## Prerequisites

- Module 5, especially L-5.1 (cell vs serving JVM), L-5.2 (clusters and `ihs-east`), and L-5.3 (`jdbc/baypay`, `BayPayBus`).
- L-4.5 (what the server owns) and L-4.4 (sessions / class loading).
- Comfort reading [datasets/baypay-cell/TOPOLOGY.md](../../../datasets/baypay-cell/TOPOLOGY.md) as the single source of names.
- JDK 21 and the Maven Wrapper for the reference app if you want to compare Boot `application-prod.yml` to Liberty variables. See [GETTING_STARTED.md](../../../GETTING_STARTED.md).

You do **not** need IBM Installation Manager, a Deployment Manager, a licensed Liberty ND collective, or a running Open Liberty JVM. Paper architecture and `server.xml` on disk cost **$0**.

---

## Lessons (30 minutes each)

Complete in order. Each lesson is self-contained; PAKS links are optional and none are required for Module 6.

| Id | Title | What it unlocks |
|---|---|---|
| [L-6.1](lessons/L-6.1.md) | Traditional WebSphere vs Liberty | ND is source; Liberty and Boot are targets |
| [L-6.2](lessons/L-6.2.md) | Liberty features and server.xml | `featureManager`, DataSource, `webApplication` |
| [L-6.3](lessons/L-6.3.md) | Compatibility assessment | Ears, JNDI, SIBus, WS-*, loaders, `javax` |
| [L-6.4](lessons/L-6.4.md) | Configuration externalization | `server.env`, variables, `BAYPAY_DB_*` |
| [L-6.5](lessons/L-6.5.md) | Migration strategy and rollback | Waves 0–3, canary, dual-run, rollback |

---

## Labs

| Id | Type | Title | After |
|---|---|---|---|
| [MODERNIZE-601](../../../labs/MODERNIZE-601/README.md) | MODERNIZE | WebSphere-to-Liberty assessment | L-6.1, L-6.3 |
| [MODERNIZE-602](../../../labs/MODERNIZE-602/README.md) | MODERNIZE | Adapt BayPay for Liberty | L-6.2, L-6.3 |
| [MODERNIZE-603](../../../labs/MODERNIZE-603/README.md) | MODERNIZE | Externalize configuration | L-6.4 |
| [ARCHITECT-604](../../../labs/ARCHITECT-604/README.md) | ARCHITECT | Migration waves and rollback | L-6.5 |

Time-box MODERNIZE labs at 60–90 minutes and ARCHITECT-604 at 60–90 minutes. You will produce files and a wave plan, not a running cell. Do not open `solutions/` until you have written the assessment or `server.xml` yourself.

---

## Assessment and portfolio

1. Complete MODERNIZE-601, MODERNIZE-602, MODERNIZE-603, and ARCHITECT-604.
2. Take [Q-06](../../quizzes/Q-06.md) (eight questions).
3. Export the assessment using [student/worksheets/PF-liberty-assessment.md](../../../student/worksheets/PF-liberty-assessment.md).

The worksheet plus the MODERNIZE-601 write-up is the Module 6 portfolio artifact: **Liberty migration assessment**. Later modules assume you can point at `BayPayCell` and explain the Liberty (or Boot) exit, isolated pools, and the wave-1 refund / wave-2 payment rollback story.

---

## Related PAKS deep dive (optional)

This module stands alone. If your cohort has a login at [paks.bayareala8s.com](https://paks.bayareala8s.com), you may skim `docs/14-microservices/service-decomposition-and-ddd.md` as background on why refund and payment are separate waves. Skip it without penalty. Course index: [PAKS_LINKS.md](../../../PAKS_LINKS.md).

---

## Guardrails

- Do not treat `BayPayCell` as a real employer architecture, a licensed IBM lab, or a real WebSphere customer topology.
- Traditional WAS ND is taught so you can **leave** it. Do not recommend a new ND cell for a blank-page BayPay service.
- Simulation-first: paper assessment, `server.xml` / `server.env` on disk, wave diagrams. Do **not** install WebSphere ND. Live Liberty is optional.
- Keep `jdbc/baypay` as the source smell. Liberty binds `jdbc/baypay-payment` and `jdbc/baypay-refund`.
- Local labs and config files cost **$0**.
- Instructor rubrics live under `instructor/rubrics/`. Students should not need them to finish the work.
- Synthetic only: Avery Chen, Harbor Bike Co, `.baypay.example` hosts, and the on-call names above.
