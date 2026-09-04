# Portfolio — Liberty migration assessment (inventory)

**Course:** Advanced Enterprise Java Engineering  
**Module:** 06  
**Lab:** MODERNIZE-601  
**Case study:** BayPay Financial Services (fictional)

Export this page (or a copy) as the assessment half of the Module 6 portfolio artifact. Pair it with [PF-liberty-waves.md](PF-liberty-waves.md) from ARCHITECT-604. Use locked names from [datasets/baypay-cell/TOPOLOGY.md](../../datasets/baypay-cell/TOPOLOGY.md) only. Traditional ND is the **source estate**. Liberty or Spring Boot is the **target**.

**Your name:**  
**Date:**  
**Cohort / reviewer (if any):**  

---

## 1. Source applications

| Ear | Cluster | Members | Context | What you will package on Liberty |
|---|---|---|---|---|
| `payment.ear` | | | | |
| `refund.ear` | | | | |

---

## 2. Dependency classification

Use exactly one primary verb per row: **lift** / **rewrite** / **defer** / **drop**. Name a Liberty feature (`servlet-6.0`, `jdbc-4.3`, `jndi-1.0`, `persistence-3.1`) or isolated bind, or `none`.

| Dependency | Type today | Scope today | Lift / rewrite / defer / drop | Liberty feature or replacement | Notes |
|---|---|---|---|---|---|
| HTTP / servlet (`payment.ear`) | | | | | |
| HTTP / servlet (`refund.ear`) | | | | | |
| EAR packaging | | | | | |
| `jdbc/baypay` | | | | | |
| `jdbc/baypayXA` | | | | | |
| `baypayDbAlias` | | | | | |
| `jms/paymentEvents` | | | | | |
| `jms/refundEvents` | | | | | |
| SIBus `BayPayBus` | | | | | |
| `ihs-east` / `plugin-cfg.xml` | | | | | |
| LTPA / cell SSO | | | | | |
| Cell-wide JNDI tree | | | | | |
| `dmgr-east` | | | | | |
| Node agents | | | | | |
| Shared pool / reporting | | | | | |
| Sticky `JSESSIONID` on `/payment` | | | | | |

Add any extra row you believe TOPOLOGY implies (class loaders, PMI, admin console). Extra rows are optional but must use locked names.

---

## 3. Isolated target binds

Write the two DataSource JNDI names you will use on Liberty and why you will **not** keep `jdbc/baypay` as a cell-wide (or server-wide shared) name.

| Target bind | Used by | Why isolated |
|---|---|---|
| | Payment WAR | |
| | Refund WAR | |

Is `3 × 50` a fact or a question until Morgan Hale confirms DataSource scope?

---

## 4. What you would NOT do for greenfield

A new BayPay service (for example an FX quote API) is requested tomorrow. In 6–10 sentences, state what you would **not** copy from `BayPayCell` (new DMGR, cell-wide `jdbc/baypay`, new SIBus, LTPA as API authn) and what you would use instead (Liberty `server.xml` with isolated DataSources, and/or the Spring Boot reference app). This paragraph is required.

---

## 5. Interview snippet (Staff, 6–8 sentences)

Explain to Morgan Hale, Jordan Voss, and a Spring engineer, in one sitting, why lifting `servlet-6.0` is not the same as lifting the cell, and why this page is an inventory of an estate you intend to leave.
