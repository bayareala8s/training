# Rubric — INCIDENT-1104 Unhealthy ALB target

**Type:** INCIDENT (awsLab)  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

A lucky “SG” (security group) with no health-path-versus-Actuator comparison must **not** max Diagnostic method (20%). HTTP 404 on the health check means the packet arrived.

| Dimension | 5 | 3 | 1 |
|---|---|---|---|
| Technical accuracy | Path `/` on port 8080 returns **404**; tasks **RUNNING**; TG unhealthy; merchants 502/503 | Unhealthy named; 404 mentioned; path fuzzy | “SG is closed” or “RDS is down” as RCA without ruling the 404 in |
| Diagnostic method | Gate 1→2→3; listener opened to confirm edge vs task; path `/` quoted | Used all files; skipped a hypothesis | Opened solutions or listener first; **or** “SG” with no timeout-vs-404 comparison |
| Production awareness | Change path to `/actuator/health/liveness`; bake into Terraform; no SG widen; no ALB delete | Restart only / bump desired count | Widen 8080 to the world, or matcher includes 404 as the lasting design |
| Trade-off analysis | BUILD-305 / ACCOUNT.md vs provider default `/`; CI fail on path `/` | Mentions Actuator | `/` as the lasting health URL |
| Security / reliability | 404 ≠ SG miss; Avery 502/503 retries; no admin IAM to “debug” | Mentions 503 | Ignores customer retries; opens 8080 publicly |
| Communication | Does not invent an SG or SQL outage; RUNNING vs healthy named | Usable, slightly over-confident | Blames “SG” in the first sentence with no reason code |
| Efficiency | 45–75 minutes | Complete but slow | Incomplete worksheet |

Stabilization that only says “restart the ECS service” without changing the health path loses Production awareness. A correct path RCA that never mentions Terraform remediation caps Production awareness at 3.
