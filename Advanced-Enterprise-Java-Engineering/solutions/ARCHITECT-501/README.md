# ARCHITECT-501 — Instructor solution

**Do not share this file with students before they submit a brief.**

## What a complete artifact contains

Locked names only. `ihs-east` is the plugin edge, not a federated node. Reporting sits on `db-east`, not inside `Pay1`. Traditional ND is documented as the **source estate**. Greenfield work is Spring Boot or Liberty — never a second `BayPayCell`.

## Reference drawing (serving + control)

```text
Merchants / Avery Chen
  HTTPS → ihs-east.baypay.example  (TLS terminate, plugin-cfg.xml, no /payment affinity)
            → PaymentCluster
                 Pay1   node-pay-1  was-pay-1.baypay.example:9080   payment.ear  /payment
                 Pay2   node-pay-2  was-pay-2.baypay.example:9080   payment.ear
                 Pay3   node-pay-2  was-pay-2.baypay.example:9081   payment.ear
            → RefundCluster
                 Ref1   node-ref-1  was-ref-1.baypay.example         refund.ear   /refund
                 Ref2   node-ref-1                                  refund.ear
              → jdbc/baypay  (+ jdbc/baypayXA where bound)
              → SIBus BayPayBus  (jms/paymentEvents, jms/refundEvents)
                 → db-east.baypay.example:5432 / baypay
                    → Reporting (nightly; own pool / own JVM)

Control: operator → dmgr-east (was-dmgr-east.baypay.example)
                 → nodeagent-pay-1 / nodeagent-pay-2 / nodeagent-ref-1
                 → application servers
```

Diagram AEJE-D-019 is this current state. Students may submit mermaid or ASCII that matches these edges.

## Clusters (expected table)

| Cluster | Member | Node | Host | Application | Context |
|---|---|---|---|---|---|
| `PaymentCluster` | `Pay1` | `node-pay-1` | `was-pay-1.baypay.example` | `payment.ear` | `/payment` |
| `PaymentCluster` | `Pay2` | `node-pay-2` | `was-pay-2.baypay.example` | `payment.ear` | `/payment` |
| `PaymentCluster` | `Pay3` | `node-pay-2` | `was-pay-2.baypay.example` | `payment.ear` | `/payment` |
| `RefundCluster` | `Ref1` | `node-ref-1` | `was-ref-1.baypay.example` | `refund.ear` | `/refund` |
| `RefundCluster` | `Ref2` | `node-ref-1` | `was-ref-1.baypay.example` | `refund.ear` | `/refund` |

Density note: `Pay2`+`Pay3` on one host is cheaper capacity, not HA. Host loss removes two of three payment members.

## JNDI and messaging

| Bind | Type | Instructor note |
|---|---|---|
| `jdbc/baypay` | DataSource, cell-scoped historically, max 50 | Shared — modernization smell. `3 × 50` is a **question** until Morgan confirms per-server pool vs one definition. |
| `jdbc/baypayXA` | XA DataSource | Incomplete; not on every node. Mixed presence is a consistency defect. |
| `jms/paymentEvents` / `jms/refundEvents` | Queue + connection | SIBus `BayPayBus`. Bus HA is whatever node hosts the ME — do not call it HA because the name includes Bus. |
| `baypayDbAlias` | J2C | Secret, not “config.” |

Reporting must not share the payment pool. Module 6 isolated names: `jdbc/baypay-payment`, `jdbc/baypay-refund`.

## Blast radius (acceptable sentences)

1. **`dmgr-east` down:** `Pay1`/`Pay2`/`Pay3`/`Ref1`/`Ref2` still serve if already STARTED. Jordan cannot install or sync. Do not bounce payment JVMs “to reset the cell.”
2. **`nodeagent-pay-2` down:** `Pay2` and `Pay3` can keep serving HTTP. Sync, remote start/stop, and distribution to `node-pay-2` are unsafe. INCIDENT-504 class of risk.
3. **`was-pay-2.baypay.example` down:** `Pay2` and `Pay3` are gone together. `Pay1` is the remaining payment member. Plugin must not keep sending to dead transports.

## Security and sessions

Three domains: merchant TLS on `ihs-east`; application authn on `payment.ear`; cell admin + LTPA keys on `BayPayCell`. `/payment` is sessionless (`Idempotency-Key` + DB). Sticky `JSESSIONID` on that URI group is a smell. Portal ears may still need sessions on a different URI group.

## Operations inset (bounce card)

Evidence first (SystemOut, FFDC, PMI, plugin membership, node-agent/sync). Drain one member at the plugin. Recycle that JVM if needed. Confirm edition + JNDI after sync. Re-add to plugin. Never bounce `dmgr-east` to fix merchant HTTP. Never bounce `db-east` because a WAS pool is full.

## Greenfield — what you would NOT do

Do not stand up a new traditional ND cell, a new SIBus, or a cell-wide shared `jdbc/baypay` for a new BayPay service. Prefer the Spring Boot reference app or Liberty `server.xml` with isolated DataSources. This brief exists so the cohort can operate and **leave** `BayPayCell`.

## Scoring notes

Full marks require locked names, IHS outside the cell, both clusters, JNDI + bus, reporting off Pay1, blast-radius sentences, sessionless `/payment`, an operations inset, and an explicit non-ND greenfield paragraph. A beautiful drawing that recommends a second DMGR caps Production awareness at 1.
