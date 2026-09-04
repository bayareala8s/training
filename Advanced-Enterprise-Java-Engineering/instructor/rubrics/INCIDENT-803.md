# Rubric — INCIDENT-803

**Type:** INCIDENT  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

A lucky “it’s a deadlock” or a pasted INC-JVM-202 worker story must **not** max Diagnostic method (20%).

| Dimension | 5 | 3 | 1 |
|---|---|---|---|
| Technical accuracy | `NightlyReversalJob` ledger→account vs `PaymentApplicationService.create` account→ledger; monitors quoted; distinct from INC-JVM-202 workers | Circular wait named; one call site fuzzy | “DB lock” or Module 2 worker names as RCA |
| Diagnostic method | Gate 1→2→3; v1 before dump; deadlock block quoted | Used all files; skipped a hypothesis | Opened solutions or the dump first |
| Production awareness | Kill the nightly job and/or bounce **that** JVM; drain canary; no Postgres / dmgr bounce | Bounce only | Bounce the database or enable the job on east-1 |
| Trade-off analysis | One lock order vs no nested locks / DB transactions; job off the API JVM | Mentions lock order | “More threads” as strategy |
| Security / reliability | Health ≠ completions; money threads must not deadlock; nightly job isolation | Mentions hung creates | Ignores in-flight Avery payment |
| Communication | Replica- and job-scoped; does not invent JDBC | Usable, slightly over-confident | Blames “deadlock” in the first sentence with no stacks |
| Efficiency | 45–75 minutes | Complete but slow | Incomplete worksheet |

Stabilization that only says “restart all JVMs” without stopping or isolating the nightly job loses Production awareness.
