# Portfolio — WebSphere ND architecture for BayPay

**Course:** Advanced Enterprise Java Engineering  
**Module:** 05  
**Lab:** ARCHITECT-501  
**Case study:** BayPay Financial Services (fictional)  
**Diagram:** AEJE-D-019 (current state)

Export this page (or a copy) as your Module 5 portfolio artifact. Use locked names from [datasets/baypay-cell/TOPOLOGY.md](../../datasets/baypay-cell/TOPOLOGY.md) only. Traditional ND is the **source estate**, not a greenfield target.

**Your name:**  
**Date:**  
**Cohort / reviewer (if any):**  

---

## 1. Cell drawing

Draw or paste mermaid/ASCII for `BayPayCell`. Must show: `dmgr-east`, `node-pay-1`, `node-pay-2`, `node-ref-1`, the three node agents, `Pay1` / `Pay2` / `Pay3`, `Ref1` / `Ref2`, and `ihs-east` **outside** the cell.

```text
(your drawing)
```

Two paths, labeled:

| Path | Hops |
|---|---|
| Serving (Avery Chen → money) | |
| Control (Morgan Hale → config) | |

---

## 2. Clusters

| Cluster | Member | Node | Host | Application | Context |
|---|---|---|---|---|---|
| `PaymentCluster` | `Pay1` | | | | |
| `PaymentCluster` | `Pay2` | | | | |
| `PaymentCluster` | `Pay3` | | | | |
| `RefundCluster` | `Ref1` | | | | |
| `RefundCluster` | `Ref2` | | | | |

Why must you **not** collapse these clusters on the drawing? What do you lose if `was-pay-2.baypay.example` dies?

---

## 3. JNDI and messaging

| Bind | Type | Scope (as you understand it) | Smell / note |
|---|---|---|---|
| `jdbc/baypay` | | | |
| `jdbc/baypayXA` | | | |
| `jms/paymentEvents` | | | |
| `jms/refundEvents` | | | |
| `baypayDbAlias` | | | |
| SIBus `BayPayBus` | | | |

Where does **reporting** sit on the drawing (same DB, not the payment pool)?  
Is `3 × 50` a fact or a question until Morgan Hale confirms DataSource scope?

---

## 4. Blast radius

| Failure | What still serves Avery Chen? | What can Jordan Voss not do? |
|---|---|---|
| `dmgr-east` down | | |
| `nodeagent-pay-2` down | | |
| Host `was-pay-2` down | | |

---

## 5. Security and sessions

| Domain | Where you placed it | What fails if it is wrong |
|---|---|---|
| Merchant TLS | | |
| Application authn | | |
| Cell admin + LTPA | | |
| DataSource secret | | |

Is `/payment` allowed to use sticky `JSESSIONID`? Why or why not?

---

## 6. Operations inset (bounce card)

Write the card in your own words (evidence → drain → recycle → confirm edition/JNDI → re-add). List two things you will **never** bounce to fix merchant HTTP.

```text
1.
2.
3.
Never:
Never:
```

---

## 7. What you would NOT do for greenfield

A new BayPay service (for example an FX quote API) is requested tomorrow. In 6–10 sentences, state what you would **not** copy from this cell (new DMGR, cell-wide `jdbc/baypay`, new SIBus, sticky payment sessions) and what you would use instead (Spring Boot reference app and/or Liberty `server.xml` with isolated DataSources). This paragraph is required.

---

## 8. Interview snippet (Staff, 6–8 sentences)

Explain to Priya Nair, Riley Okonkwo, and a Spring engineer, in one sitting, why `STARTED` is not throughput, why `ihs-east` is not a node, and why this page is an inventory of an estate you intend to leave.
