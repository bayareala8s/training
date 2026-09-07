# Portfolio — Liberty migration waves and rollback

**Course:** Advanced Enterprise Java Engineering  
**Module:** 06  
**Lab:** ARCHITECT-604  
**Case study:** BayPay Financial Services (fictional)  
**Diagram:** AEJE-D-027

Export this page (or a copy) with [PF-liberty-assessment.md](PF-liberty-assessment.md) as the Module 6 portfolio pair. Wave numbers and rollback one-liners must match [datasets/baypay-cell/TOPOLOGY.md](../../datasets/baypay-cell/TOPOLOGY.md). Traditional ND is the **source estate**. Liberty or Spring Boot is the **target**. Do not invent a Wave 4 that stands up a second `BayPayCell`.

**Your name:**  
**Date:** 2026-09-06  
**Cohort / reviewer (if any):**  

---

## 1. Wave table (0–3)

| Wave | Scope (your words, locked names) | Success signal | Rollback | Who calls rollback (role) |
|---|---|---|---|---|
| 0 | Inventory + compatibility (MODERNIZE-601). Classify `payment.ear` / `refund.ear` binds. No merchant traffic moves. No Liberty replica in `plugin-cfg.xml`. | Assessment page complete: isolated names decided, SIBus not “lifted,” `dmgr-east` marked drop, greenfield refusal written. | N/A | Riley Okonkwo (application on-call) — can **halt** Wave 1 start if blockers are still open; there is nothing to restore. |
| 1 | `refund-service.war` on Liberty (`jdbc/baypay-refund`, `BAYPAY_DB_*`). Context `/refund` behind `ihs-east`. `refund.ear` stays **installed** on `RefundCluster` (`Ref1`, `Ref2` on `node-ref-1`). Lower volume than payment. Dual-run optional; many plans flip refund 100% after a short bake because blast is small. | `/refund` error rate and p99 hold vs the ND baseline; Liberty logs show isolated bind (not `jdbc/baypay`); `Ref1`/`Ref2` still STARTED and unused or standby. | Restore `refund.ear` on `RefundCluster`; plugin `/refund` back to `Ref1`/`Ref2`; stop Liberty refund weight. | Riley Okonkwo (application on-call). Morgan Hale executes plugin + ear start. Do not page Jordan to “reinstall the cell.” |
| 2 | **One** Liberty `/payment` replica (`payment-service.war`, `jdbc/baypay-payment`) behind `ihs-east` beside `Pay1`/`Pay2`/`Pay3`. Dual-run: two runtimes, one idempotent API, one `baypay` database, **two pools**. Low plugin weight. Not a flip of `PaymentCluster`. | Canary 5xx and p99 within hold; synthetic Avery path 201; `Idempotency-Key` replay matches ND; canary pool waiters ~0; ND members still serve the majority. | Drain the canary; **100% `PaymentCluster`**. Leave Wave 1 refund on Liberty unless `/refund` is also failing. | Riley Okonkwo (money path). Priya Nair confirms 100% ND at `ihs-east`. Morgan changes plugin weight. |
| 3 | After SLO hold: drain remaining ND serving; stop `Pay1`/`Pay2`/`Pay3` / `Ref1`/`Ref2` / node agents; then retire `dmgr-east`. Decommission `node-pay-1`, `node-pay-2`, `node-ref-1`. | Holds in §5 stay green for the named bake. Last ND backup exists and is restore-tested on paper. | Keep last ND backup until **wave 3 + 14 days**. You cannot undecommission if you deleted the cell the same afternoon. | Priya Nair (SRE) — only she calls “hold failed, restore from backup.” Jordan Voss does not delete backups the night SLO turns green. |

Wave 1 names `refund.ear` / `RefundCluster`. Wave 2 is a **single** Liberty payment replica, not a big-bang cut of `Pay1`/`Pay2`/`Pay3`. Wave 3 keeps a last ND backup until **wave 3 + 14 days**. No Wave 4 / `BayPayCell-2`.

---

## 2. Wave 1 rollback card (refund)

Write the card in your own words. Assume Harbor Market refund volume is already on Liberty `refund-service.war` and error rate or latency breaches the hold.

```text
Evidence to collect:
  /refund 5xx and p99 vs ND baseline (Priya). Liberty SystemOut / messages.log:
  jdbc/baypay-refund checkout failures, missing feature, or JMS if someone
  pretended SIBus lifted. Confirm RefundCluster Ref1/Ref2 still STARTED
  (Morgan) — ear must still be installed.

Drain / traffic action at ihs-east:
  Set Liberty refund member weight 0 (or remove from plugin-cfg.xml).
  Send 100% of /refund to Ref1 and Ref2. Not sticky JSESSIONID.

Restore on ND:
  Start refund.ear on RefundCluster if it was stopped. Do not bounce
  dmgr-east. Do not rebuild the ear from Git as the first move.

Confirm:
  POST /refund 2xx on Ref1 or Ref2. Context root /refund. Harbor Market
  refund that failed on Liberty can retry (same business key).

Re-enter Liberty only when:
  Named hold: refund error rate back to baseline on ND for 24h, RCA written
  (bind / messaging / feature — not “restarted Liberty”), and Wave 0
  blockers that bit us are re-scored.

Never:
  Bounce dmgr-east to “reset refunds.” Uninstall refund.ear in Wave 1.
  Bounce db-east. Stand up a second cell. Re-enter the same night without a hold.
```

What exactly is restored onto `RefundCluster`?

**`refund.ear`** (already installed from Wave 1 on purpose) on **`Ref1` and `Ref2`**, context `/refund`, still using the cell bind the ear already has (`jdbc/baypay` on ND — we are leaving that smell on the source estate, not copying it forward). Rollback is **plugin + start**, not a rebuild.

---

## 3. Wave 2 rollback card (payment canary)

Avery Chen (`11111111-1111-1111-1111-111111111111`) may be in the canary bucket. Write the card so money stays on `PaymentCluster` if the Liberty replica misbehaves.

```text
Evidence to collect:
  Payment 5xx / p99 on the canary member vs Pay1/Pay2/Pay3. Connection
  wait or NameNotFound on jdbc/baypay-payment. Idempotent replay mismatch
  (same Idempotency-Key 201 then 500 or a second ledger row). Avery
  c504-class “works on retry to ND” is enough to drain — do not wait for
  a cluster-wide page.

Drain the canary (plugin / IHS):
  Weight 0 or delete liberty-pay-canary:9080 from plugin-cfg.xml.
  Confirm ihs-east lists only Pay1, Pay2, Pay3 for /payment.

What stays at 100%:
  PaymentCluster (Pay1, Pay2, Pay3) on node-pay-1 / node-pay-2.
  Wave 1 Liberty /refund stays up if refund SLOs hold.

What you do not bounce:
  dmgr-east. db-east. Pay1 (someone will ask — no: the canary is the
  defect, not ND). node-pay-2 as a node (would take Pay2 and Pay3 down).

Confirm edition / JNDI on ND:
  All three members same last-known-good edition (INC-WAS-504 lesson).
  Cell jdbc/baypay still serves ND payment. Canary must not have been
  bound to jdbc/baypay.

Re-enter canary only when:
  Named hold: PaymentCluster 5xx flat for 24h; canary RCA is bind / feature
  / probe (not TCP-only STARTED); Idempotency-Key contract re-tested on
  both runtimes with Avery 11111111-1111-1111-1111-111111111111.

Never:
  Flip Pay1/Pay2/Pay3 to Liberty in the same window. Enable sticky
  JSESSIONID so Avery “stays on the canary.” Bounce dmgr-east. Delete
  PaymentCluster because the canary looked green for an hour.
```

Is “bounce `dmgr-east`” on this card? It must not be.

**No.** Serving path is `ihs-east` → members. `dmgr-east` is control plane. Drain works from the plugin file even if the console is down.

If **both** URI groups fail: drain **payment** first (money still majority on ND), then restore refund routing if needed. Documented order of *procedures* is still refund-card then payment-card; the commander picks the bleeding URI.

---

## 4. Routing and isolation

| Question | Your answer |
|---|---|
| How does `ihs-east` send a fraction of `/payment` to the Liberty canary without sticky `JSESSIONID`? | Add **one** member (`liberty-pay-canary:9080`) to the `/payment` ServerCluster with a **low weight**. Majority weight stays on `Pay1`/`Pay2`/`Pay3`. Round-robin / weighted routing. Retries use `Idempotency-Key` + the shared ledger, not JVM affinity. Do not enable sticky sessions “to make the canary simpler.” Probes must check feature start + JNDI `jdbc/baypay-payment` + a synthetic POST — not TCP-only (INC-WAS-502). |
| What JNDI name does the canary use? | `jdbc/baypay-payment` |
| What JNDI name must the canary **not** reuse from the cell? | `jdbc/baypay` (cell-scoped). Also do not add `jdbc/baypayXA`. Database is shared; pools are not. Dual-run on one name is INC-WAS-503 again. |
| Where do `BAYPAY_DB_*` values live for the canary? | Liberty `server.env` / process env / later platform secret. XML has only `${env.BAYPAY_DB_HOST\|PORT\|NAME\|USER\|PASSWORD}`. No password in Git. Same *key names* as Boot `application-prod.yml`; different pool than ND `baypayDbAlias`. |
| What happens to `jms/paymentEvents` during Wave 2 if you deferred SIBus? | `PaymentCluster` still uses SIBus `BayPayBus` / `jms/paymentEvents`. The Liberty canary **does not** lift the bus. HTTP create/post on the canary uses the isolated JDBC path (and in-process / Boot-style events if the WAR already does). Rollback of HTTP does **not** require a bus restore. Do not create a Liberty messaging engine and call Wave 2 done. |

---

## 5. SLO hold before Wave 3

List three measurable holds (availability, latency, refund error rate, or payment idempotent replay) that must stay green before Jordan Voss decommissions `node-pay-1` / `node-pay-2` / `node-ref-1`. Name the 14-day backup rule.

```text
1. /payment availability and 5xx: Liberty (now majority or 100% after a later
   raise) holds the ND baseline for a named bake (e.g. 14 days of Wave 2
   at full weight, or the Wave 3 entry bake — Priya owns the number).
2. /payment p99 and idempotent replay: same Idempotency-Key against Avery
   11111111-1111-1111-1111-111111111111 does not double-post; frozen account
   22222222-2222-2222-2222-222222222222 still denied on both stories before
   ND is gone.
3. /refund error rate + p99 stay at or below the Wave 1 ND baseline for the
   same bake. No open “we will fix SIBus after we delete Ref1.”

Backup retained until:
  Wave 3 + 14 days. Last dmgr-east / node repository backup, restore-tested
  on paper. Decommission is stop Pay*/Ref*/node agents then dmgr-east —
  not “delete backups tonight.” Git has server.xml; Git does not restore
  the cell repository, LTPA, or plugin history if you must walk ND back.
```

---

## 6. What you would NOT do

In 6–10 sentences: no new traditional ND cell as a “safe rollback environment,” no cell-wide `jdbc/baypay` on Liberty, no SIBus recreation, no sticky payment sessions to make the canary “simpler.” Name Boot or Liberty as the exit.

I would **not** stand up `BayPayCell-2` (or a “rollback cell”) because Morgan asks for safety. Safety is plugin drain, ears left installed through Wave 2, and a 14-day ND backup — not a second Deployment Manager. I would **not** bind cell-wide `jdbc/baypay` on any Liberty replica so the canary “matches lookups”; that is INC-WAS-503 with a new process. I would **not** recreate SIBus `BayPayBus` on Liberty or invent a new traditional bus for greenfield. I would **not** enable sticky `JSESSIONID` on `/payment` so Avery stays on the canary; retries are idempotent, not sessionful. I would **not** flip `Pay1`/`Pay2`/`Pay3` in one window, uninstall `refund.ear` in Wave 1, bounce `dmgr-east` to reset traffic, or delete backups the night the SLO turns green. I would **not** treat the Boot teaching app as a wave target. Exit is Liberty `server.xml` for ears that must stay Jakarta wars this quarter, or Spring Boot 3.5.5 for blank-page services — both beat a new ND cell.

---

## 7. Interview snippet (Staff, 6–8 sentences)

Explain to Priya Nair, Riley Okonkwo, and Morgan Hale why Wave 1 is refund, why Wave 2 is a canary rather than a cluster flip, and why Wave 3 is not “delete the cell tonight.”

Wave 1 is refund because Harbor Market refund volume lives on `RefundCluster` (`Ref1`/`Ref2` on `node-ref-1`) and is smaller than Avery’s `/payment` traffic. We rehearse leave-and-restore on the cheap URI first: `refund.ear` stays installed so rollback is plugin + start, not a Friday rebuild. Wave 2 is **one** Liberty `/payment` replica behind `ihs-east` because Avery’s volume is not a rehearsal — a cluster flip of `Pay1`/`Pay2`/`Pay3` is a Sev-1 with no ND majority to drain back to. If the canary 5xx’s, the first sentence is “drain the canary; do not bounce `Pay1`.” Morgan still owns `dmgr-east` and plugin regen through Wave 2; Priya owns the SLO hold; Riley calls rollback on the money path. Wave 3 waits until those holds stay green, then we decommission nodes — and we keep the last ND backup until wave 3 + 14 days, because Git cannot restore a cell you deleted tonight.
