# Rubric — INCIDENT-1205

**Type:** INCIDENT  
**awsLab:** yes (files only)  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

A lucky “bad deploy” or “rollback” with no quoted **9080** versus **8080** and no quoted tags must **not** max Diagnostic method (20%).

| Dimension | 5 | 3 | 1 |
|---|---|---|---|
| Technical accuracy | Image `3.8.9-debug` listens on **9080**; TG/health on **8080**; circuit breaker rolled to **`payment-service:80` / 3.8.0**; pipeline green without tests/smoke | Named a tag or a port; one side quoted | “Postgres down” or “IAM” as RCA without contrast |
| Diagnostic method | Gate 1→2→3; pipeline before deployments; both ports and both tags quoted | Used all files; skipped a hypothesis | Opened solutions or `task-def-diff.txt` first |
| Production awareness | Stabilize on **3.8.0 / revision 80**; no `:latest` push; no DB bounce; no ALB retarget to 9080 | Restart service only | Push `:latest` or scale to zero |
| Trade-off analysis | Pipeline smoke on **8080** vs circuit breaker; immutable tags vs `:latest` | Mentions smoke or tags | Treats rollback as the only fix forever |
| Security / reliability | Avery 502 retries; no invented secret change; least-privilege describe/update | Mentions 502 | Ignores customer retries or invents `BAYPAY_DB_PASSWORD` |
| Communication | Green CI vs unhealthy TG named; does not invent a DB outage | Usable, slightly over-confident | Blames “ECS” with no revision or port |
| Efficiency | 45–75 minutes; no live AWS | Complete but slow | Incomplete worksheet or live apply to “reproduce” |

Stabilization that only says “redeploy the debug tag” while revision 80 is already healthy loses Production awareness.

**Pass guideline:** weighted score ≥ 70, both ports quoted, stabilize = last healthy 3.8.0, remediate includes smoke on 8080 and no `:latest`.
