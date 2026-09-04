# Rubric — INCIDENT-504

**Type:** INCIDENT  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

A lucky “sync failed” with no edition table and no JNDI name must **not** max Diagnostic method (20%).

| Dimension | 5 | 3 | 1 |
|---|---|---|---|
| Technical accuracy | Pay1 4.12 expects `jdbc/baypayXA`; Pay2/Pay3 still 4.11; install during `nodeagent-pay-2` restart; intermittent `NameNotFoundException` | Mixed versions named; missing XA or sync incomplete | “Bad code” or “JNDI is down” as RCA |
| Diagnostic method | Gate 1→2→3; deployment history opened to confirm/refute a written question | Used all files; skipped a hypothesis | Opened solutions or history first |
| Production awareness | One edition on all members (rollback Pay1 **or** finish sync + bind XA); no dual-direction thrash | Finish the install without a bind plan | Bounce `db-east` or keep mixed editions “until Monday” |
| Trade-off analysis | Rollback vs forward cost; roll servers not the `was-pay-2` host; canary must hit more than Pay1 | Mentions rolling deploys | Feature-flag talk with no edition discipline |
| Security / reliability | Missing bind as fail-closed (good) vs mixed contract (bad); idempotent retries across editions | Mentions naming errors | Ignores split-brain money responses |
| Communication | Member- and edition-scoped; does not name XA before quoting it | Usable, slightly over-confident | “Deploy succeeded” because the cell checkbox is green |
| Efficiency | 45–75 minutes | Complete but slow | Incomplete worksheet |

Stabilization that continues 4.12 on Pay1 while Pay2/Pay3 stay 4.11 loses Production awareness even if the student later writes a good gate.
