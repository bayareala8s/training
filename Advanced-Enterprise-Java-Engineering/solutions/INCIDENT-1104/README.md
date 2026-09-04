# INCIDENT-1104 — Instructor solution

**Do not share this file with students before they submit a worksheet.**

## RCA

ALB target group `baypay-1101-tg` health check is **`Path=/`** on **port 8080**. Spring Boot `payment-service` returns **404** on `/` (no static index). Matcher expects **200**. Targets are **unhealthy**. ECS tasks stay **`RUNNING`** (`containerPort` 8080, no exit). The listener forwards to that target group. Merchants see **502/503**.

This is the BUILD-1101 starter defect left in place: the provider default health path is `/`. ACCOUNT.md and BUILD-305 require `/actuator/health/liveness`.

This is **not** a security-group miss. A 404 means the health-check packet arrived and the JVM answered. An SG / wrong-port failure would be a timeout or connection refused, not HTTP 404.

This is not INCIDENT-1003 (kubelet readiness). Same *class* of contract miss, different object. This is not a database-down readiness (404 on `/`, not a `DOWN` body on `/actuator/health/readiness`). RDS was not in the student apply.

## Stabilization

1. Change the target-group health check **path** to **`/actuator/health/liveness`** (matcher `200`, port `8080`).
2. Wait for healthy targets. Do not accept `404` in the matcher “so it goes green.”
3. Do **not** open task SG 8080 to `0.0.0.0/0`.
4. Do not bounce RDS or `dmgr-east`.
5. Do not delete the ALB.
6. Do not set `desired_count = 0` and back to 1 as the fix.

## Remediation

- Bake `health_check.path = "/actuator/health/liveness"` into the Terraform module (solutions/BUILD-1101). Do not rely on the provider default `/`.
- CI: fail a plan when the path is `/` or `/health`.
- Keep `/` off the matcher. Operators can still curl Actuator; the ALB must not treat a 404 homepage as liveness.
- Document the contract in ACCOUNT.md / PF-aws-platform.md so the next starter cannot ship `/`.

## Evidence students should have used

| Gate | What it shows |
|---|---|
| target-health.txt | Unhealthy; port 8080; **Path=/**; **HTTP 404**; matcher 200 |
| task-def.json | `lastStatus: RUNNING`; `containerPort` 8080; no exit |
| alb-listener.txt | :80 forward to the same TG; merchant **503** (clients also 502) |

A worksheet that says only “SG” or only “unhealthy ALB” without quoting **Path=/** versus Actuator scores poorly on Diagnostic method even if the lab title matches.

## Comms (acceptable example)

SEV-2 on `pay-alb-student.baypay.example`. ECS tasks are RUNNING. The ALB target group health check on `/` returns 404, so targets are unhealthy and merchants see 502/503. We are changing the health path to `/actuator/health/liveness`. We are not opening security groups and not bouncing a database. Next update 20 minutes.
