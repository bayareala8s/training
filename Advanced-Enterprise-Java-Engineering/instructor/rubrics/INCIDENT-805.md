# Rubric — INCIDENT-805

**Type:** INCIDENT  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

A lucky “excessive GC” or “it’s a leak” with no allocation-versus-retained story must **not** max Diagnostic method (20%).

| Dimension | 5 | 3 | 1 |
|---|---|---|---|
| Technical accuracy | DEBUG overlay; `Payment.toString()` / graph logging; ~1.8 GB/s; young pauses hundreds of ms; ephemeral `String`/`[C]`; **not** 802 | Pauses + DEBUG named; mechanism fuzzy | “Tune G1” or “same leak as 802” as RCA |
| Diagnostic method | Gate 1→2→3; histogram opened to answer retained-vs-churn; quotes | Used all files; skipped a hypothesis | Opened solutions or the histogram first |
| Production awareness | Revert log level; no collector swap; no Postgres bounce | Bounce canary only | Bounce the database or set DEBUG on east-1 |
| Trade-off analysis | No entity `toString` on hot path; rate-limit DEBUG; sampling vs global level | Mentions log volume | `MaxGCPauseMillis` as strategy |
| Security / reliability | DEBUG in prod as an availability risk; PII in graph dumps noted | Mentions stalls | Leaves DEBUG on “until Avery is found” |
| Communication | Replica-scoped; does not announce a leak the old-gen chart contradicts | Usable, slightly over-confident | Blames “GC” in the first sentence with no rate |
| Efficiency | 45–75 minutes | Complete but slow | Incomplete worksheet |

Stabilization that only says “restart all JVMs” without reverting DEBUG loses Production awareness.
