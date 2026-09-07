# Portfolio — WebSphere ND architecture for BayPay

**Course:** Advanced Enterprise Java Engineering  
**Module:** 05  
**Lab:** ARCHITECT-501  
**Case study:** BayPay Financial Services (fictional)  
**Diagram:** AEJE-D-019 (current state)

Export this page (or a copy) as your Module 5 portfolio artifact. Use locked names from [datasets/baypay-cell/TOPOLOGY.md](../../datasets/baypay-cell/TOPOLOGY.md) only. Traditional ND is the **source estate**, not a greenfield target.

**Your name:**  
**Date:** 2026-09-06  
**Cohort / reviewer (if any):**  

---

## 1. Cell drawing

Draw or paste mermaid/ASCII for `BayPayCell`. Must show: `dmgr-east`, `node-pay-1`, `node-pay-2`, `node-ref-1`, the three node agents, `Pay1` / `Pay2` / `Pay3`, `Ref1` / `Ref2`, and `ihs-east` **outside** the cell.

```text
Merchants / Avery Chen
        │ HTTPS
        ▼
 ihs-east.baypay.example     ← TLS + plugin-cfg.xml   (NOT a WAS node)
        │
        ├── /payment (no JSESSIONID affinity) ──► Pay1   Pay2   Pay3
        └── /refund                           ──► Ref1   Ref2

 BayPayCell
   dmgr-east @ was-dmgr-east.baypay.example
        │  sync / admin only
        ├── nodeagent-pay-1 @ node-pay-1 / was-pay-1.baypay.example
        │         └── Pay1  payment.ear  /payment
        ├── nodeagent-pay-2 @ node-pay-2 / was-pay-2.baypay.example
        │         ├── Pay2  payment.ear  /payment
        │         └── Pay3  payment.ear  /payment      ← same host as Pay2
        └── nodeagent-ref-1 @ node-ref-1 / was-ref-1.baypay.example
                  ├── Ref1  refund.ear   /refund
                  └── Ref2  refund.ear   /refund

 JNDI (cell-scoped historically): jdbc/baypay  jdbc/baypayXA?
                                   jms/paymentEvents  jms/refundEvents
                                   baypayDbAlias
 SIBus BayPayBus  (ME lives on a node — same AD as that host)

                    jdbc/*  ──►  db-east.baypay.example:5432 / baypay
                                      └── Reporting (nightly; NOT inside Pay1)
```

Two paths, labeled:

| Path | Hops |
|---|---|
| Serving (Avery Chen → money) | Client → `ihs-east` (TLS, `plugin-cfg.xml`) → `Pay1`/`Pay2`/`Pay3` or `Ref1`/`Ref2` → `jdbc/baypay` / `BayPayBus` → `db-east:5432` |
| Control (Morgan Hale → config) | Operator → `dmgr-east` → `nodeagent-*` → application server. Merchants never hit `dmgr-east`. |

---

## 2. Clusters

| Cluster | Member | Node | Host | Application | Context |
|---|---|---|---|---|---|
| `PaymentCluster` | `Pay1` | `node-pay-1` | `was-pay-1.baypay.example` | `payment.ear` | `/payment` |
| `PaymentCluster` | `Pay2` | `node-pay-2` | `was-pay-2.baypay.example` | `payment.ear` | `/payment` |
| `PaymentCluster` | `Pay3` | `node-pay-2` | `was-pay-2.baypay.example` | `payment.ear` | `/payment` |
| `RefundCluster` | `Ref1` | `node-ref-1` | `was-ref-1.baypay.example` | `refund.ear` | `/refund` |
| `RefundCluster` | `Ref2` | `node-ref-1` | `was-ref-1.baypay.example` | `refund.ear` | `/refund` |

Why must you **not** collapse these clusters on the drawing? What do you lose if `was-pay-2.baypay.example` dies?

Payment and refund are separate ears, pools, and rollouts. Collapsing them hides that Harbor Market refunds can live while payment members are drained, and that Jordan deploys `payment.ear` independently of `refund.ear`.

`was-pay-2` down takes **Pay2 and Pay3** together (density bought, correlated failure spent). Avery still has **Pay1** only on the payment side — one third of payment JVMs, not “the cell is down.” Refunds on `node-ref-1` are untouched.

---

## 3. JNDI and messaging

| Bind | Type | Scope (as you understand it) | Smell / note |
|---|---|---|---|
| `jdbc/baypay` | DataSource | Cell-scoped historically | Shared pool is a modernization smell. Incident-default `maxConnections = 50`. |
| `jdbc/baypayXA` | XA DataSource | **Not on every node** | Incomplete / failed-deploy leftover. Do not assume Pay1–Pay3 all have it. |
| `jms/paymentEvents` | Queue + CF | Cell / `BayPayBus` | In-process Boot events are the teaching equivalent; this is the ND name. |
| `jms/refundEvents` | Queue + CF | Cell / `BayPayBus` | Same bus as payment — one AD. |
| `baypayDbAlias` | J2C auth alias | Cell | Username/password for the DataSource — not “the database.” |
| SIBus `BayPayBus` | Messaging engine | Lives on a node | ME host down = bus down for that engine. Do not add a new bus for greenfield. |

Where does **reporting** sit on the drawing (same DB, not the payment pool)?  
Beside `db-east`, as a nightly client. Not a module in `Pay1`. Same lesson as INCIDENT-402: settlement SQL does not checkout `jdbc/baypay`.

Is `3 × 50` a fact or a question until Morgan Hale confirms DataSource scope?  
A **question**. If `jdbc/baypay` is cell-scoped one pool, three payment members share **50**. If application- or server-scoped, it could be `3 × 50` into `db-east`. Ask Morgan Hale before you raise max or size `max_connections`.

---

## 4. Blast radius

| Failure | What still serves Avery Chen? | What can Jordan Voss not do? |
|---|---|---|
| `dmgr-east` down | `ihs-east` → Pay1–Pay3 / Ref1–Ref2 still serve. HTTP 201 can continue. | No admin console, no sync, no new deploy/edition. “The cell is down” is the wrong first sentence. |
| `nodeagent-pay-2` down | Pay2 and Pay3 **keep running** if they were already up. Pay1 + refunds serve. | Cannot sync, start/stop, or push a new ear to Pay2/Pay3. `STARTED` may be stale vs edition. |
| Host `was-pay-2` down | Pay1 only for `/payment`. Refunds unchanged. | Lost two payment JVMs at once. Do not bounce `dmgr-east` or `db-east` to “fix” that. |

---

## 5. Security and sessions

| Domain | Where you placed it | What fails if it is wrong |
|---|---|---|
| Merchant TLS | `ihs-east` terminates HTTPS | Clients fail handshake; ears should not own public certs |
| Application authn | `payment.ear` / `refund.ear` | 401/403 on `/payment` — not an IHS outage |
| Cell admin + LTPA | `dmgr-east` / cell LTPA keys | Priya cannot admin; merchant HTTP can still work |
| DataSource secret | `baypayDbAlias` (J2C) | Pool auth failures; do not put the password in the ear |

Is `/payment` allowed to use sticky `JSESSIONID`? Why or why not?

**No.** Creates are idempotent (`Idempotency-Key`), not session-sticky. Affinity hides a bad Pay2 behind one merchant, fights rolling deploys, and is not required for Avery’s POST. Plugin may support stickiness; we refuse it on `/payment`.

---

## 6. Operations inset (bounce card)

Write the card in your own words (evidence → drain → recycle → confirm edition/JNDI → re-add). List two things you will **never** bounce to fix merchant HTTP.

```text
1. Evidence first: plugin-cfg route, PMI pool (active/waiters), FFDC, which member, which ear edition.
2. Drain one member from ihs-east (remove from plugin / weight 0). Do not drain the cell.
3. Recycle that one JVM. Confirm START and the same payment.ear edition + JNDI as Pay1.
4. Re-add to the plugin. Watch p99 and jdbc waiters on that member only.
Never: bounce dmgr-east to fix merchant HTTP (wrong plane).
Never: bounce db-east because a WAS pool is full (INCIDENT-402 shape — kill the holder, do not restart Postgres).
```

---

## 7. What you would NOT do for greenfield

A new BayPay service (for example an FX quote API) is requested tomorrow. In 6–10 sentences, state what you would **not** copy from this cell (new DMGR, cell-wide `jdbc/baypay`, new SIBus, sticky payment sessions) and what you would use instead (Spring Boot reference app and/or Liberty `server.xml` with isolated DataSources). This paragraph is required.

I would not stand up a second traditional ND cell, a new `dmgr`, or another federated node for FX quotes. I would not bind the new service to cell-wide `jdbc/baypay` or invent `jdbc/baypayXA` “for later.” I would not add a queue to `BayPayBus` or create a new SIBus so FX shares the payment messaging engine’s blast radius. I would not enable sticky `JSESSIONID` on a write API. Greenfield is the Spring Boot monolith we already run (`BAYPAY_DB_*` in YAML, isolated process) or Liberty with `server.xml` + `server.env` and **isolated** DataSources (`jdbc/baypay-payment`, `jdbc/baypay-refund` in the Module 6 target). Traditional `BayPayCell` stays inventory we operate until the migration waves — it is not a pattern to copy.

---

## 8. Interview snippet (Staff, 6–8 sentences)

Explain to Priya Nair, Riley Okonkwo, and a Spring engineer, in one sitting, why `STARTED` is not throughput, why `ihs-east` is not a node, and why this page is an inventory of an estate you intend to leave.

`STARTED` on Pay2 means the JVM accepted a start; it does not mean it is on the same `payment.ear` edition as Pay1, or that the plugin is sending it Avery’s POSTs, or that `jdbc/baypay` waiters are zero. `ihs-east` is the TLS and `plugin-cfg.xml` edge — it is not federated into `BayPayCell` and it is not `dmgr-east`. Merchants depend on IHS plus cluster members; Priya can lose the admin console and still see HTTP 201. JNDI is the **name** (`jdbc/baypay`, `baypayDbAlias`); the database is `db-east`. This page is how we operate the source estate without bouncing the wrong process, and how we refuse a new ND cell when Harbor Bike asks for FX quotes tomorrow.
