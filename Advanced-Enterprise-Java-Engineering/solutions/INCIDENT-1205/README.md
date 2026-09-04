# INCIDENT-1205 — Instructor solution

**Do not share this file with students before they submit a worksheet.**

## RCA

CI (Jordan Voss, BAYPAY-12051) deployed image tag **`3.8.9-debug`**. That process listens on **9080** (`SERVER_PORT=9080`, `BAYPAY_DEBUG_LISTENER=liberty-compat-9080`). ECS/ALB target group `pay-alb-student-tg` still probes **HTTP 8080** `/actuator/health/liveness`. Tasks register, fail health, and the **deployment circuit breaker rolls back** to last healthy task definition **`payment-service:80`** / image **`3.8.0`**.

The pipeline job was **green** because there was **no test job** and **no image smoke**. The workflow also pushed **`:latest`**. This is not a Postgres outage and not an IAM/secret miss. The prior revision is already PRIMARY and healthy after rollback.

## Stabilization

1. **Leave** (or confirm) the service on **`payment-service:80`** / **`baypay/payment-service:3.8.0`**. If the roll is still stuck on revision 88, `update-service --task-definition payment-service:80` (or the console equivalent) and wait for 2/2 healthy.
2. Confirm target group health on **8080** / `/actuator/health/liveness`, then retest `pay-alb-student.baypay.example`.
3. Do **not** push another `:latest` from a laptop.
4. Do not bounce Postgres or `dmgr-east`.
5. Do not change the ALB to 9080 “so the debug image can stay.”
6. Do not scale the service to zero.

## Remediation

- **Pipeline smoke:** after `docker build`, GET `http://127.0.0.1:8080/actuator/health/liveness` (or `curl` in the image) **before** `ecs update-service`. Fail the job if the process is not on **8080**.
- Restore the BUILD-1204 **test** job (`Java 21`, `./mvnw test`) so publish cannot be the only job.
- **Immutable tags only** — `${{ github.sha }}` or `3.8.0`. **Never `:latest`** as a deploy tag. Prefer ECR `IMMUTABLE`.
- Refuse `*-debug` tags (or `SERVER_PORT` overrides) in the prod task family without a matching target-group change reviewed as a two-object change.
- Circuit breaker `enable=true` / `rollback=true` stays on; it is not a substitute for smoke.

## Evidence students should have used

| Gate | What it shows |
|---|---|
| pipeline.log | Tag `3.8.9-debug` and `:latest`; **test job skipped**; **smoke skipped**; ECS deploy of revision 88; workflow **success** |
| ecs-deployments.txt | Circuit breaker **rollback**; tasks **unhealthy on port 8080**; TG path `/actuator/health/liveness`; last healthy **`payment-service:80`** / **3.8.0** |
| task-def-diff.txt | Image `3.8.9-debug`; **`SERVER_PORT=9080`**; containerPort still 8080; healthCheck still curls **8080**; 80 had `SERVER_PORT=8080` |

A worksheet that says only “bad deploy” or “rollback” without quoting **9080** versus **8080** and the two tags scores poorly on Diagnostic method even if the lab title matches.

## Comms (acceptable example)

SEV-2 on `pay-alb-student.baypay.example`. ALB 502 after the main pipeline. New tasks failed target-group health on 8080. Circuit breaker rolled back to task definition 80 / image 3.8.0. We are confirming 2/2 healthy and not bouncing the database. Next update 20 minutes.

## Diagram

AEJE-D-057: CI tag → ECS → ALB health fail → circuit breaker → prior task definition.
