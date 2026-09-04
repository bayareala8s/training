# Rubric — MODERNIZE-601

**Type:** MODERNIZE  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

A classification from memory that lifts cell-scoped `jdbc/baypay` as-is, or a brief that recommends a new traditional ND cell, must not outscore a disciplined TOPOLOGY-based page.

| Dimension | 5 | 3 | 1 |
|---|---|---|---|
| Technical accuracy | Both ears; every TOPOLOGY JNDI/messaging row; isolated `jdbc/baypay-payment` / `jdbc/baypay-refund`; SIBus dropped as a product; DMGR dropped | Most rows right; one lift/rewrite swap | Invented binds; JNDI called “the database”; SIBus lifted |
| Diagnostic method | Walked TOPOLOGY.md (and 601 worksheet) before classifying; `3 × 50` treated as a question | Skimmed the mermaid only | Opened `solutions/` first; classified from memory |
| Production awareness | ND as source estate; Boot/Liberty as target; IHS kept; reporting not on the payment pool | Mentions Liberty without a stance | Recommends a new traditional ND cell |
| Trade-off analysis | Messaging API ≠ SIBus product; XA deferred/dropped with a reason; Liberty vs Boot when an ear must stay | One honest trade-off | All rows treated as identical lifts |
| Security / reliability | `baypayDbAlias` as a secret; LTPA not used as `/payment` authn; sessionless payment | Mentions secrets or LTPA | LTPA as the payment API credential |
| Communication | Brief a Staff engineer could reuse | Readable table, thin narrative | Fragment notes |
| Efficiency | 60–90 minutes, complete `PF-liberty-assessment.md` | Complete but unfocused | Incomplete worksheet |

A greenfield WAS / second-DMGR recommendation caps Production awareness at 1 regardless of table quality. Lifting `jdbc/baypay` as the same cell-wide name caps Technical accuracy at 3 or below.
