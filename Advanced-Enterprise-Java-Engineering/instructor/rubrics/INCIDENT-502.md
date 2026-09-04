# Rubric — INCIDENT-502

**Type:** INCIDENT  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

A lucky “hung threads” or “plugin is wrong” with no gate order must **not** max Diagnostic method (20%) and must **not** outscore a disciplined write-up.

| Dimension | 5 | 3 | 1 |
|---|---|---|---|
| Technical accuracy | Pay2/Pay3 STARTED but not processing; Pay1 healthy; stale `jdbc/baypay` after the blip; TCP probe keeps them in rotation | Exhaustion or hung threads named; mechanism fuzzy | “The cluster is down” or “Postgres is down” as RCA |
| Diagnostic method | Gate 1→2→3; hung-thread lines treated as candidates until stacks and plugin view | Used all files; skipped a hypothesis | Opened solutions or all evidence first |
| Production awareness | Drain Pay2/Pay3 at `ihs-east`; recycle those JVMs only; leave Pay1, DMGR, and `db-east` | Bounce all of `PaymentCluster` | Bounce the database or `dmgr-east` |
| Trade-off analysis | HTTP plugin health vs TCP; hung-thread policy vs interrupt; drain-two cost on a shared host | Mentions health checks | Raise every max as strategy |
| Security / reliability | Connection validation as a control; retries + idempotency noted | Timeouts mentioned | Ignores customer retries landing on dead members |
| Communication | Member-scoped, no unsupported cause | Usable, slightly over-confident | Blames “the hang” in the first sentence with no evidence |
| Efficiency | 45–75 minutes | Complete but slow | Incomplete worksheet |

Stabilization that only says “restart the cell” without removing Pay2/Pay3 from the plugin loses Production awareness.
