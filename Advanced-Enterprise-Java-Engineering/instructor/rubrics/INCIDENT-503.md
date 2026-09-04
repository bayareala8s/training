# Rubric — INCIDENT-503

**Type:** INCIDENT  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

A lucky “it’s the pool” or “50/50” with no occupant and no gate order must **not** max Diagnostic method (20%).

| Dimension | 5 | 3 | 1 |
|---|---|---|---|
| Technical accuracy | Pay1 50/50; `reporting.ear` on `node-pay-1` holds `jdbc/baypay`; DB CPU low; Pay2/Pay3 spare | Exhaustion named; occupant fuzzy | “Postgres is down” or “raise max to 200” as RCA |
| Diagnostic method | Gate 1→2→3; PMI opened to answer a written question | Used all files; skipped a hypothesis | Opened solutions or PMI first |
| Production awareness | Stop reporting on payment nodes; recycle Pay1 only if needed | Bounce all payment JVMs | Bounce the database |
| Trade-off analysis | Rejects raising `max` as first fix; isolate DataSources; reporting off payment JVMs | Mentions sizing | Pool max as strategy |
| Security / reliability | Shared cell-scoped name as a reliability smell; retries + idempotency noted | Timeouts mentioned | Ignores that reporting can starve money traffic |
| Communication | JVM-scoped, does not name reporting before evidence | Usable, slightly over-confident | Blames “the leak” or “the pool” with no holder |
| Efficiency | 45–75 minutes | Complete but slow | Incomplete worksheet |

Stabilization that only says “restart Pay1” without stopping `reporting.ear` loses Production awareness.
