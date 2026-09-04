# Rubric — INCIDENT-1003

**Type:** INCIDENT  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

A lucky “readiness” with no probe-path-versus-Actuator comparison must **not** max Diagnostic method (20%).

| Dimension | 5 | 3 | 1 |
|---|---|---|---|
| Technical accuracy | Ready 0/1; Running; readiness `/actuator/health/readiness` **404**; liveness `/actuator/health` 200; Endpoints empty; Ingress 503 | Readiness named; 404 mentioned; path fuzzy | “Postgres is down” or “selector mismatch” as RCA without ruling 1006 out |
| Diagnostic method | Gate 1→2→3; curl opened to confirm edge vs pod; describe quoted | Used all files; skipped a hypothesis | Opened solutions or curl first |
| Production awareness | Fix probe path or add readiness group; no DB bounce; no Ingress delete | Restart only | Bounce Postgres or use `/health` as both probes permanently without a note |
| Trade-off analysis | BUILD-305 groups vs aggregate health; CI curl of probe paths | Mentions Actuator | Single `/actuator/health` as the lasting design |
| Security / reliability | Running ≠ traffic; Avery 503 retries; heapdump still off | Mentions 503 | Ignores customer retries |
| Communication | Does not invent a CrashLoop; Ready vs Running named | Usable, slightly over-confident | Blames “503” in the first sentence with no Endpoints |
| Efficiency | 45–75 minutes | Complete but slow | Incomplete worksheet |

Stabilization that only says “restart the Deployment” without changing path or image groups loses Production awareness.
