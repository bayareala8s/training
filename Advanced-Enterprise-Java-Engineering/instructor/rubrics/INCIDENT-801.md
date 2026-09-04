# Rubric — INCIDENT-801

**Type:** INCIDENT  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

A lucky “it’s a regex” or “CPU spin” with no gate order must **not** max Diagnostic method (20%).

| Dimension | 5 | 3 | 1 |
|---|---|---|---|
| Technical accuracy | 3.8.1 canary on `pay-prod-east-2`; `String.matches` on full POST body in `RequestBodyPiiScanner`; east-1 3.8.0 healthy; not GC/heap | CPU named; canary vs stable; mechanism fuzzy | “Database is down” or “need more cores” as RCA |
| Diagnostic method | Gate 1→2→3; dump opened to answer a written question; Pattern frames quoted | Used all files; skipped a hypothesis | Opened solutions or the dump first |
| Production awareness | Remove canary from LB or revert 3.8.1; no east-1 roll; no Postgres bounce | Bounce the canary only | Bounce the database or fail over the region |
| Trade-off analysis | Linear parser or delete scan vs `matches()` on unbounded JSON; size cap | Mentions “fix the regex” | Scale Tomcat / add replicas as strategy |
| Security / reliability | PII scan still needed, but not at the cost of matching the whole body; canary gate on CPU/p99 | Mentions body inspection | Disables all compliance checks with no replacement |
| Communication | Replica-scoped; does not name a regex cause before quoting stacks | Usable, slightly over-confident | Blames “the CPU” in the first sentence with no evidence |
| Efficiency | 45–75 minutes | Complete but slow | Incomplete worksheet |

Stabilization that only says “restart all JVMs” without taking 3.8.1 out of the pool loses Production awareness.
