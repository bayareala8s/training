# ARCHITECT-604 — Instructor solution

**Do not share this file with students before they submit wave cards.**

The compact table in the student lab is a *post-attempt* numbering check. It is not the scored narrative. A worksheet that only pastes TOPOLOGY’s four rows must not outscore a plan with owners, evidence, and rollback cards.

Traditional ND is the **source estate** you roll back **onto**. Liberty or Spring Boot is the **target**. Do not create `BayPayCell-2` as a “safe” environment.

## Locked wave table (expanded)

| Wave | Scope | Success signal | Rollback | Owner |
|---|---|---|---|---|
| 0 | Inventory + compatibility (MODERNIZE-601). Classify JNDI, SIBus, LTPA, plugin. No traffic move. | Assessment page names isolated binds; greenfield sentence refuses a new ND cell | N/A | Jordan Voss + Morgan Hale (inventory) |
| 1 | `refund-service.war` on Liberty with `jdbc/baypay-refund`. `RefundCluster` (`Ref1`, `Ref2`) stays installed. Lower volume than payment. | `/refund` SLO hold (error rate + latency) on Liberty; ND refund ear still startable | Restore `refund.ear` on `RefundCluster`; drain Liberty refund at `ihs-east` | Riley Okonkwo (app) / Priya Nair (edge) |
| 2 | **One** Liberty payment replica behind `ihs-east` with `jdbc/baypay-payment`. `Pay1`/`Pay2`/`Pay3` remain. Sessionless `/payment`. | Canary error rate and idempotent replay match ND; pool not shared with reporting | Drain canary; 100% `PaymentCluster` | Priya Nair (plugin) / Riley (payments) |
| 3 | Decommission `node-pay-1`, `node-pay-2`, `node-ref-1` after SLO hold. `dmgr-east` last. | Payment + refund SLOs green for the hold window | Keep last ND backup until **wave 3 + 14 days**; restore from backup if needed — do not invent a new cell | Jordan Voss (release) / Morgan Hale (cell teardown) |

## Wave 1 rollback card (acceptable content)

Evidence first: `/refund` 5xx, Liberty logs, plugin membership, refund DB errors — not “the cell feels slow.” Drain Liberty refund members at `ihs-east` / `plugin-cfg.xml`. Restore `refund.ear` on `RefundCluster` (`Ref1`, `Ref2` on `node-ref-1`). Confirm context `/refund` and that `jdbc/baypay` still serves ND refund (source estate). Re-enter Liberty after a named hold. Never bounce `dmgr-east` to fix merchant refund HTTP. Never bounce `db-east` because a Liberty pool is empty.

## Wave 2 rollback card (acceptable content)

Evidence first: payment 5xx on the canary, idempotency conflicts that ND does not show, canary DataSource errors. Drain **only** the Liberty payment replica at the plugin. 100% of `/payment` returns to `PaymentCluster`. Avery Chen may retry; `Idempotency-Key` plus the database make affinity unnecessary. Do not bounce `Pay1` “to match the canary.” Do not bounce `dmgr-east`. Do not bounce `db-east`. Confirm ND edition and cell bind still serve. Re-enter the canary after a named hold and a config diff (`jdbc/baypay-payment`, `${env.BAYPAY_DB_*}`).

## Routing and isolation

`ihs-east` stays the edge. Plugin weights or a dedicated Liberty member in `plugin-cfg.xml` send a fraction of `/payment` to the canary. No sticky `JSESSIONID`. Canary JNDI is `jdbc/baypay-payment`. Forbidden: cell-wide `jdbc/baypay` on Liberty. Credentials live in `server.env` / runtime `BAYPAY_DB_PASSWORD`, not XML.

If JMS was deferred in MODERNIZE-601: `PaymentCluster` still uses `jms/paymentEvents` on `BayPayBus`. The canary must not claim it lifted SIBus. HTTP canary plus ND events is an honest interim; a silent in-process event is an approximation (ARCHITECT-401).

## Wave 3 hold

Accept any three measurable holds, for example: payment availability, payment p99, refund error rate, idempotent replay equality versus ND. Last ND backup retained until wave 3 + 14 days. Git is not that backup (it does not restore LTPA keys, plugin members, or a known-good `payment.ear` 4.11/4.12 pair).

## Greenfield — what you would NOT do

No second traditional ND cell as a rollback environment. No cell-wide `jdbc/baypay` on Liberty. No new SIBus. No sticky payment sessions to make the canary simpler. Exit is Liberty `server.xml` or the Spring Boot reference app.

## Diagram

AEJE-D-027: waves 0→1→2→3 with rollback arrows to `RefundCluster` and to 100% `PaymentCluster`, plus the 14-day backup.

## Scoring notes

Full marks require expanded waves (not paste-only), Wave 1 restore-ear language, Wave 2 drain-canary language, no DMGR bounce, sessionless payment, isolated JNDI in the routing inset, 14-day backup, and a non-ND greenfield paragraph. Wave 1 as payment, or Wave 2 as a full cluster flip, caps Technical accuracy and Production awareness.
