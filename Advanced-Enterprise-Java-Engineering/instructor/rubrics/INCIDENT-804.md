# Rubric — INCIDENT-804

**Type:** INCIDENT  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

A lucky “thread-pool exhaustion” with no waiter and no downstream must **not** max Diagnostic method (20%).

| Dimension | 5 | 3 | 1 |
|---|---|---|---|
| Technical accuracy | Tomcat 200/200 `WAITING` on `FxQuoteClient`; pool 8; no timeout; `fx-east` hung; Hikari/DB fine | HTTP pool named; FX mentioned; mechanism fuzzy | “Postgres is down” or “set Tomcat to 2000” as RCA |
| Diagnostic method | Gate 1→2→3; dump opened to answer a written question; waiter quoted | Used all files; skipped a hypothesis | Opened solutions or the dump first |
| Production awareness | Fail-open/skip FX or shed canary; no Tomcat 2000; no Postgres bounce | Bounce canary only | Bounce the database or raise Tomcat max as the fix |
| Trade-off analysis | Timeouts + bulkhead + breaker; FX off the USD create path | Mentions timeout | Bigger inbound pool as strategy |
| Security / reliability | Fail-open vs skip; money path must not depend on a decorative quote | Mentions hung creates | Ignores Avery retries |
| Communication | Replica-scoped; does not blame the database the gauges contradict | Usable, slightly over-confident | Blames “thread pool” in the first sentence with no waiter |
| Efficiency | 45–75 minutes | Complete but slow | Incomplete worksheet |

Stabilization that only says “restart all JVMs” or “max=2000” loses Production awareness.
