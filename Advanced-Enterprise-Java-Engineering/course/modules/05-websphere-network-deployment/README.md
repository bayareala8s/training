# Module 5 — WebSphere Network Deployment

**Duration:** ~3 hours of lessons plus 4 labs  
**Case study:** BayPay Financial Services (fictional)  
**Theme:** BayPay on traditional WebSphere ND  
**Portfolio artifact:** WebSphere ND architecture for BayPay from [ARCHITECT-501](../../../labs/ARCHITECT-501/README.md)

BayPay is a fictional payments company used throughout this course. It is not a real bank, card network, or employer. Every customer, account, hostname, dump, and metric you see is synthetic.

**Delivery note:** this module is **architecture plus incident simulation**. A live WebSphere ND cell is **not** required. You will design from paper, read dumps, and write an RCA. You will not install Deployment Manager, federate nodes, or start a node agent on your laptop.

---

## Business context

BayPay’s **source estate** is a traditional WebSphere Network Deployment cell named `BayPayCell`. Merchants still hit `payment.ear` on `PaymentCluster` and `refund.ear` on `RefundCluster`. IBM HTTP Server `ihs-east` terminates TLS and forwards with `plugin-cfg.xml`. The cell owns JDBC, JNDI, SIBus, class loaders, and cluster membership so the ears can stay thin.

That topology is **not** a greenfield recommendation. New BayPay work belongs on Spring Boot (the teaching runtime in `reference-apps/baypay/`) or on Liberty in Module 6. You study ND so you can operate it until cutover, diagnose it without bouncing the wrong JVM, and leave it without rebuilding a cell in Kubernetes.

The locked inventory lives in [datasets/baypay-cell/TOPOLOGY.md](../../../datasets/baypay-cell/TOPOLOGY.md). Reuse those names in every diagram, lab, and interview answer:

| Role | Locked name |
|---|---|
| Cell | `BayPayCell` |
| Deployment manager | `dmgr-east` on `was-dmgr-east.baypay.example` |
| Payment nodes | `node-pay-1`, `node-pay-2` |
| Refund node | `node-ref-1` |
| Payment cluster | `PaymentCluster` members `Pay1`, `Pay2`, `Pay3` |
| Refund cluster | `RefundCluster` members `Ref1`, `Ref2` |
| Applications | `payment.ear` (`/payment`), `refund.ear` (`/refund`) |
| DataSource | `jdbc/baypay` (cell-scoped historically) |
| Messaging | SIBus `BayPayBus`, `jms/paymentEvents`, `jms/refundEvents` |
| Edge | `ihs-east` / `ihs-east.baypay.example` |

Demo identities remain:

| Role | Synthetic id |
|---|---|
| Customer Avery Chen | `11111111-1111-1111-1111-111111111111` |
| Active USD account | `22222222-2222-2222-2222-222222222221` |
| Frozen USD account | `22222222-2222-2222-2222-222222222222` |

On-call names used in dumps: **Priya Nair** (SRE), **Riley Okonkwo** (application on-call), **Morgan Hale** (WAS cell administrator), **Jordan Voss** (release engineer).

---

## Learning objectives

After this module you can:

- Draw `BayPayCell` as cell → DMGR → node → node agent → application server, and say what still serves payments when `dmgr-east` is down.
- Place `PaymentCluster` (`Pay1`/`Pay2`/`Pay3`) and `RefundCluster` (`Ref1`/`Ref2`) behind `ihs-east`, and contrast a rolling deploy with a completed node sync.
- Explain cell-scoped `jdbc/baypay` and `jms/paymentEvents` on `BayPayBus`, and why a shared pool is a modernization smell.
- Size web-container threads against a WAS JDBC pool of `maxConnections = 50`, and describe hung-thread policy as a signal — not a bounce button.
- State why the payment API must stay sessionless, why sticky sessions are a smell, and where IHS SSL and LTPA sit on the path.
- Operate from FFDC, PMI, node-agent health, and `plugin-cfg.xml` without installing ND, and produce a portfolio architecture for BayPay.

---

## Prerequisites

- Modules 1–4, especially L-4.3 (pools), L-4.4 (sessions / class loading), and L-4.5 (what the server owns).
- Comfort reading [datasets/baypay-cell/TOPOLOGY.md](../../../datasets/baypay-cell/TOPOLOGY.md) as the single source of names.
- JDK 21 and the Maven Wrapper for the reference app if you want to compare Boot config to cell bindings. See [GETTING_STARTED.md](../../../GETTING_STARTED.md).

You do **not** need IBM Installation Manager, a Deployment Manager profile, or network access to a cell. Paper architecture and incident packs cost **$0**.

---

## Lessons (30 minutes each)

Complete in order. Each lesson is self-contained; PAKS links are optional and none are required for Module 5.

| Id | Title | What it unlocks |
|---|---|---|
| [L-5.1](lessons/L-5.1.md) | Cell, DMGR, node, node agent and server | Who owns config vs who serves Avery Chen |
| [L-5.2](lessons/L-5.2.md) | Clusters and deployments | `PaymentCluster`, IHS plugin, rollout vs sync |
| [L-5.3](lessons/L-5.3.md) | JDBC, JNDI and JMS | `jdbc/baypay`, `BayPayBus`, cell vs app scope |
| [L-5.4](lessons/L-5.4.md) | JVM configuration and pools | Threads, `maxConnections=50`, hung-thread policy |
| [L-5.5](lessons/L-5.5.md) | Security, SSL and sessions | IHS SSL, LTPA, sessionless payment API |
| [L-5.6](lessons/L-5.6.md) | Operations and troubleshooting | FFDC, PMI, plugin-cfg, what to bounce |

---

## Labs

| Id | Type | Title | After |
|---|---|---|---|
| [ARCHITECT-501](../../../labs/ARCHITECT-501/README.md) | ARCHITECT | Design WebSphere ND BayPay | L-5.1, L-5.2, L-5.3 |
| [INCIDENT-502](../../../labs/INCIDENT-502/README.md) | INCIDENT | Cluster members stop processing | L-5.4, L-5.6 |
| [INCIDENT-503](../../../labs/INCIDENT-503/README.md) | INCIDENT | JDBC pool exhaustion | L-5.3, L-5.4 |
| [INCIDENT-504](../../../labs/INCIDENT-504/README.md) | INCIDENT | Deployment failure | L-5.2, L-5.6 |

Time-box ARCHITECT-501 at 60–90 minutes and incident labs at 45–75 minutes. INCIDENT-502, INCIDENT-503, and INCIDENT-504 do **not** include the root cause in the student guide. You will diagnose from symptoms and dumps. Do not open `solutions/` until you have written a hypothesis from evidence.

---

## Assessment and portfolio

1. Complete ARCHITECT-501 and the three incidents.
2. Take [Q-05](../../quizzes/Q-05.md) (eight questions).
3. Export the cell architecture using [student/worksheets/PF-was-nd.md](../../../student/worksheets/PF-was-nd.md).

The worksheet plus the ARCHITECT-501 diagram is the Module 5 portfolio artifact: **WebSphere ND architecture for BayPay**. Capstone 2 and Module 6 will assume you can point at `BayPayCell` and explain why Liberty (or Boot) is the exit, not a second DMGR.

---

## Related PAKS deep dive (optional)

Lessons stand alone. If your cohort has a login at [paks.bayareala8s.com](https://paks.bayareala8s.com), optional background:

- `docs/12-messaging-and-streaming/overview.md` (SIBus / events literacy — not a Kafka mandate)
- `docs/27-production-failures/overview.md` (operate-to-leave, not a new cell)

Skip them without penalty. Curated index: [PAKS_LINKS.md](../../../PAKS_LINKS.md).

---

## Guardrails

- Do not treat `BayPayCell` as a real employer architecture or a licensed IBM lab.
- Traditional WAS ND is taught for **modernization literacy**. Do not recommend a new ND cell for a blank-page BayPay service.
- Simulation-first: design, read dumps, write RCAs. Do **not** install WebSphere ND.
- Local labs and incident packs cost **$0**.
- Instructor rubrics live under `instructor/rubrics/`. Students should not need them to finish the work.
- Synthetic only: Avery Chen, Harbor Bike Co, `.baypay.example` hosts, and the on-call names above.
