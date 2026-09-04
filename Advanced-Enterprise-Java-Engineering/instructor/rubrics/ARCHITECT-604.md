# Rubric — ARCHITECT-604

**Type:** ARCHITECT  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

The compact wave table in the student lab is a *post-attempt* hint. Using it as the first draft of `PF-liberty-waves.md` without cards caps Diagnostic method. A plan that recommends a new traditional ND cell as rollback must not outscore a TOPOLOGY-based page.

| Dimension | 5 | 3 | 1 |
|---|---|---|---|
| Technical accuracy | Waves 0–3 locked; Wave 1 restores `refund.ear` on `RefundCluster`; Wave 2 drains one canary to 100% `PaymentCluster`; 14-day backup | Waves numbered; one rollback thin | Wave 1 is payment; Wave 2 flips all payment members; invented Wave 4 cell |
| Diagnostic method | Expanded TOPOLOGY (owners, evidence, cards) after 601 classifications | Pasted the four-line table and added a sentence | Opened `solutions/` first; paste-only |
| Production awareness | ND as rollback *target* then exit; IHS routing; isolated JNDI on the canary; no DMGR bounce | Mentions rollback without owners | New ND cell as “safe rollback environment” |
| Trade-off analysis | Refund-first vs payment-first; Liberty vs Boot for Wave 1; plugin canary vs DNS cut; Git ≠ ND backup | One honest trade-off | Big-bang as simpler |
| Security / reliability | Sessionless `/payment`; `BAYPAY_DB_*` not in XML; canary must not use `jdbc/baypay` | Mentions secrets or sessions | Sticky `JSESSIONID` as the canary strategy |
| Communication | Cards a Staff engineer could run at 02:00 | Readable table, thin cards | Fragment notes |
| Efficiency | 60–90 minutes, complete `PF-liberty-waves.md` | Complete but unfocused | Incomplete worksheet |

A greenfield WAS / second-DMGR recommendation caps Production awareness at 1 regardless of table quality. Wave 2 as a full `PaymentCluster` cutover caps Technical accuracy at 3 or below.
