# BayPay WebSphere ND cell — synthetic current state

**Fictional.** BayPay Financial Services is not a real employer. Hostnames use `.baypay.example`. No live cell is required for this course.

This file is the locked topology for Modules 5–6. Lessons, labs, incidents, and diagrams must reuse these names.

## Philosophy

Traditional WebSphere ND is BayPay’s **source estate**. Teach it so engineers can operate, diagnose, and **leave** it. Do not recommend a new ND cell for greenfield work. Liberty (or the Spring Boot reference app) is the modernization target.

## Network path

```text
Merchants / Avery Chen clients
  → IHS / load balancer  ihs-east.baypay.example  (plugin-cfg.xml)
    → PaymentCluster  (payment.ear)
    → RefundCluster   (refund.ear)
      → SIBus BayPayBus  (jms/paymentEvents, jms/refundEvents)
        → PostgreSQL-compatible  db-east.baypay.example:5432 / baypay
          → Reporting (nightly, should not share the payment pool)
```

Greenfield / teaching runtime remains `reference-apps/baypay` (Spring Boot 3.5.5, Java 21).

## Cell inventory

| Role | Name | Host |
|---|---|---|
| Cell | `BayPayCell` | — |
| Deployment manager | `dmgr-east` | `was-dmgr-east.baypay.example` |
| Node | `node-pay-1` | `was-pay-1.baypay.example` |
| Node | `node-pay-2` | `was-pay-2.baypay.example` |
| Node | `node-ref-1` | `was-ref-1.baypay.example` |
| Node agent | `nodeagent-pay-1` | on `node-pay-1` |
| Node agent | `nodeagent-pay-2` | on `node-pay-2` |
| Node agent | `nodeagent-ref-1` | on `node-ref-1` |
| IHS / plugin | `ihs-east` | `ihs-east.baypay.example` |

## Clusters and JVMs

| Cluster | Members | Node | Application |
|---|---|---|---|
| `PaymentCluster` | `Pay1` | `node-pay-1` | `payment.ear` context `/payment` |
| `PaymentCluster` | `Pay2` | `node-pay-2` | `payment.ear` |
| `PaymentCluster` | `Pay3` | `node-pay-2` | `payment.ear` |
| `RefundCluster` | `Ref1` | `node-ref-1` | `refund.ear` context `/refund` |
| `RefundCluster` | `Ref2` | `node-ref-1` | `refund.ear` |

## JNDI and messaging (cell-scoped unless a lab says otherwise)

| Bind | Type | Notes |
|---|---|---|
| `jdbc/baypay` | DataSource | Shared historically — a modernization smell |
| `jdbc/baypayXA` | XA DataSource | Added in some failed deploys; not on every node |
| `jms/paymentEvents` | Queue connection + queue | SIBus `BayPayBus` |
| `jms/refundEvents` | Queue connection + queue | SIBus `BayPayBus` |
| J2C alias | `baypayDbAlias` | Username/password for the DataSource |

WAS JDBC pool (PaymentCluster default in incidents): **maxConnections = 50**.

## Demo identities (same as Modules 1–4)

| Role | Value |
|---|---|
| Customer Avery Chen | `11111111-1111-1111-1111-111111111111` |
| Active USD account | `22222222-2222-2222-2222-222222222221` |
| Frozen USD account | `22222222-2222-2222-2222-222222222222` |
| Merchant | Harbor Bike Co / Harbor Market (synthetic) |

## People (synthetic)

| Name | Role |
|---|---|
| Priya Nair | SRE |
| Riley Okonkwo | Application on-call |
| Morgan Hale | WAS cell administrator |
| Jordan Voss | Release engineer |

## Liberty target (Module 6)

- Runtime: Open Liberty / WebSphere Liberty (paper + `server.xml`; no licensed ND install)
- Features students should expect: `servlet-6.0`, `jdbc-4.3`, `jndi-1.0`, `persistence-3.1`
- App packaging: `payment-service.war` / `refund-service.war` (or the Boot fat JAR stays Boot)
- Config: `server.xml` + `server.env` / variables — no cell-wide JNDI tree
- Isolated DataSources: `jdbc/baypay-payment`, `jdbc/baypay-refund` (do not keep one cell-wide pool)

## Migration waves (ARCHITECT-604)

| Wave | Scope | Rollback |
|---|---|---|
| 0 | Inventory + compatibility assessment | N/A |
| 1 | Refund on Liberty (lower volume) | Restore `refund.ear` on `RefundCluster` |
| 2 | Payment canary (one Liberty replica behind IHS) | Drain canary; 100% `PaymentCluster` |
| 3 | Decommission ND nodes after SLO hold | Keep last ND backup until wave 3+14 days |

## What students must not do

- Install a live WebSphere ND cell
- Treat this topology as a real employer architecture
- Recommend traditional ND for a new BayPay service
- Put RCA in incident student guides
