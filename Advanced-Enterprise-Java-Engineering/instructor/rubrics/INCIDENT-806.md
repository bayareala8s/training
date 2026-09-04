# Rubric — INCIDENT-806

**Type:** INCIDENT  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

A lucky “container OOM” with no flag-versus-limit comparison must **not** max Diagnostic method (20%).

| Dimension | 5 | 3 | 1 |
|---|---|---|---|
| Technical accuracy | 512Mi limit; `-Xmx512m` (100%); cgroup `OOMKilled` exit 137; heap used ~400 MB; native+threads+metaspace; not Java OOME first | OOMKilled named; Xmx vs limit mentioned; mechanism fuzzy | “Java heap leak” or “bounce Postgres” as RCA |
| Diagnostic method | Gate 1→2→3; flags opened to answer heap-vs-cgroup; events quoted | Used all files; skipped a hypothesis | Opened solutions or flags first |
| Production awareness | Raise limit **or** drop Xmx (e.g. 75%) and restart; never Xmx==limit again; no DB bounce | Restart only | Set new Xmx equal to a new limit |
| Trade-off analysis | `MaxRAMPercentage` vs reviewed `-Xmx` with headroom; who owns the number when the limit changes | Mentions headroom | “Use all the RAM” as strategy |
| Security / reliability | Availability during restart bursts; idempotent retries; canary resize needs a flag review | Mentions 502s | Ignores Avery retries |
| Communication | Replica-scoped; does not claim a Java OOME the events contradict | Usable, slightly over-confident | Blames “OOM” in the first sentence with no limit |
| Efficiency | 45–75 minutes | Complete but slow | Incomplete worksheet |

Stabilization that only says “restart the pod” without changing limit or heap pairing loses Production awareness.
