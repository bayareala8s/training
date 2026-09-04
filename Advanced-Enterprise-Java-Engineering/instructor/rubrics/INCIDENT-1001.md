# Rubric — INCIDENT-1001

**Type:** INCIDENT  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

A lucky “CrashLoop” or “bad ConfigMap” with no Exit-code-plus-bind comparison must **not** max Diagnostic method (20%).

| Dimension | 5 | 3 | 1 |
|---|---|---|---|
| Technical accuracy | CrashLoop; Exit 1; bind / ApplicationContext; `BAYPAY_DB_URL` dropped from `payment-config`; image pulled | CrashLoop named; ConfigMap mentioned; key fuzzy | “Postgres is down” or “bad image” as RCA |
| Diagnostic method | Gate 1→2→3; ConfigMap opened to answer env question; logs quoted | Used all files; skipped a hypothesis | Opened solutions or ConfigMap first |
| Production awareness | Restore key or revert revision; no DB bounce; no image bake | Restart only | Bounce Postgres or `dmgr-east` |
| Trade-off analysis | Required env in schema vs optional URL; dry-run boot | Mentions required keys | Bake URL into the image as strategy |
| Security / reliability | Fail-fast on missing URL; Avery retries / idempotency noted | Timeouts mentioned | Ignores customer retries |
| Communication | Namespace-scoped; does not invent a SQL outage | Usable, slightly over-confident | Blames “CrashLoop” in the first sentence with no Exit code |
| Efficiency | 45–75 minutes | Complete but slow | Incomplete worksheet |

Stabilization that only says “restart the pods” without restoring the ConfigMap contract loses Production awareness.
