# Rubric — INCIDENT-402

**Type:** INCIDENT  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

A lucky “it’s a leak” with no gate order must **not** outscore a disciplined write-up.

| Dimension | 5 | 3 | 1 |
|---|---|---|---|
| Technical accuracy | Exhaustion on `pay-prod-east-2`; unclosed preview connections / EM; DB not down | Exhaustion named; mechanism fuzzy | “Postgres is down” or “raise max to 200” as RCA |
| Diagnostic method | Gate 1→2→3; leak-detection treated as candidate until stacks | Used all files; skipped a hypothesis | Opened solutions or all evidence first |
| Production awareness | Bounce one replica; stop the job; other replicas serving | Bounce everything | Bounce the database |
| Trade-off analysis | Rejects raising `max` as first fix; reporting off API pool | Mentions sizing | Pool max as strategy |
| Security / reliability | Checkout cap / leak threshold as controls; retries + idempotency noted | Timeouts mentioned | Ignores customer retries |
| Communication | Replica-scoped, no unsupported cause | Usable, slightly over-confident | Blames “the leak” in the first sentence with no evidence |
| Efficiency | 45–75 minutes | Complete but slow | Incomplete worksheet |

Stabilization that only says “restart all JVMs” without stopping the preview job loses Production awareness.
