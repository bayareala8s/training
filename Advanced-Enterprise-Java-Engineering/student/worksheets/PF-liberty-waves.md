# Portfolio — Liberty migration waves and rollback

**Course:** Advanced Enterprise Java Engineering  
**Module:** 06  
**Lab:** ARCHITECT-604  
**Case study:** BayPay Financial Services (fictional)  
**Diagram:** AEJE-D-027

Export this page (or a copy) with [PF-liberty-assessment.md](PF-liberty-assessment.md) as the Module 6 portfolio pair. Wave numbers and rollback one-liners must match [datasets/baypay-cell/TOPOLOGY.md](../../datasets/baypay-cell/TOPOLOGY.md). Traditional ND is the **source estate**. Liberty or Spring Boot is the **target**. Do not invent a Wave 4 that stands up a second `BayPayCell`.

**Your name:**  
**Date:**  
**Cohort / reviewer (if any):**  

---

## 1. Wave table (0–3)

| Wave | Scope (your words, locked names) | Success signal | Rollback | Who calls rollback (role) |
|---|---|---|---|---|
| 0 | | | N/A | |
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

Wave 1 must name `refund.ear` / `RefundCluster`. Wave 2 must name a **single** Liberty payment replica behind `ihs-east`, not a big-bang cut of `Pay1`/`Pay2`/`Pay3`. Wave 3 must keep a last ND backup until **wave 3 + 14 days**.

---

## 2. Wave 1 rollback card (refund)

Write the card in your own words. Assume Harbor Market refund volume is already on Liberty `refund-service.war` and error rate or latency breaches the hold.

```text
Evidence to collect:
Drain / traffic action at ihs-east:
Restore on ND:
Confirm:
Re-enter Liberty only when:
Never:
```

What exactly is restored onto `RefundCluster`?

---

## 3. Wave 2 rollback card (payment canary)

Avery Chen (`11111111-1111-1111-1111-111111111111`) may be in the canary bucket. Write the card so money stays on `PaymentCluster` if the Liberty replica misbehaves.

```text
Evidence to collect:
Drain the canary (plugin / IHS):
What stays at 100%:
What you do not bounce:
Confirm edition / JNDI on ND:
Re-enter canary only when:
Never:
```

Is “bounce `dmgr-east`” on this card? It must not be.

---

## 4. Routing and isolation

| Question | Your answer |
|---|---|
| How does `ihs-east` send a fraction of `/payment` to the Liberty canary without sticky `JSESSIONID`? | |
| What JNDI name does the canary use? | |
| What JNDI name must the canary **not** reuse from the cell? | |
| Where do `BAYPAY_DB_*` values live for the canary? | |
| What happens to `jms/paymentEvents` during Wave 2 if you deferred SIBus? | |

---

## 5. SLO hold before Wave 3

List three measurable holds (availability, latency, refund error rate, or payment idempotent replay) that must stay green before Jordan Voss decommissions `node-pay-1` / `node-pay-2` / `node-ref-1`. Name the 14-day backup rule.

```text
1.
2.
3.
Backup retained until:
```

---

## 6. What you would NOT do

In 6–10 sentences: no new traditional ND cell as a “safe rollback environment,” no cell-wide `jdbc/baypay` on Liberty, no SIBus recreation, no sticky payment sessions to make the canary “simpler.” Name Boot or Liberty as the exit.

---

## 7. Interview snippet (Staff, 6–8 sentences)

Explain to Priya Nair, Riley Okonkwo, and Morgan Hale why Wave 1 is refund, why Wave 2 is a canary rather than a cluster flip, and why Wave 3 is not “delete the cell tonight.”
