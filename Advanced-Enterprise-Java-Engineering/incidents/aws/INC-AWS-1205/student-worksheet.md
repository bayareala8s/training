# INC-AWS-1205 student worksheet

Fill in order. Quote evidence. Do not paste instructor solutions.

**Incident:** Failed ECS deploy after a green pipeline  
**Cluster / region:** `baypay-prod-west` / `us-west-2`  
**Your name / cohort:**  
**Time started:** 2026-09-07  
**Time submitted:** 2026-09-07  

## Current hypothesis

(What do you think is happening? Update after each gate.)

Gate 1: Pipeline **green is not a health gate**. Job **test skipped** (no test job — BUILD-1204 starter shape). Publish built `baypay/payment-service:3.8.9-debug` **and** `:latest` from `main` sha `c0ffee1205…`. **No smoke** (“Harbor Market wants this tag now”). Registered **`payment-service:88`**, `update-service` to 88, workflow success 21:56Z. Deploy tag is a **debug** name, not `${{ github.sha }}`. Next: ECS deployments — is PRIMARY 88 failing ALB health / circuit-breaker rolling back? Quote TG path/port. Then task-def-diff only to compare 88 vs last healthy revision (port, image, health).

Gate 2: Circuit breaker **rolled back**. Deployment 88 **FAILED** (`ELB_HEALTH_CHECK_FAILURE`, 4 failed tasks). **PRIMARY is `payment-service:80`**, image **`3.8.0`**, RUNNING 2/2. TG `pay-alb-student-tg` is already ACCOUNT.md: HTTP **8080** `/actuator/health/liveness` — **not** INC-1104 (`/`). Tasks 88-a/88-b unhealthy **on port 8080**. Process 88 did not satisfy 8080 liveness. Question for gate 3: does revision **88** (`3.8.9-debug`) set `containerPort` / listen to something **other than 8080** (debug **9080**?) while 80 stays 8080 / `3.8.0`?

Gate 3: Yes. **88** image `3.8.9-debug`, `SERVER_PORT=9080` (+ `BAYPAY_DEBUG_LISTENER=liberty-compat-9080`). **80** image `3.8.0`, `SERVER_PORT=8080`. `containerPort` still **8080** on both; TG and container `healthCheck` still curl **8080**. JVM listens on **9080**; ALB/health hit **8080** → unhealthy → circuit breaker → **80**. Green CI never tested listen port. RCA is port contract, not Postgres, not IAM, not a missing TG path.

## Supporting evidence

(File, timestamp, quote. Pipeline tag, health check, task definition fields.)

- `timeline.json` 21:48Z Jordan BAYPAY-12051 “fast tag.” 21:56Z workflow success. 22:04Z Priya 502, TG failing; pipeline + deployments before Postgres. 22:07Z pager. 22:08Z Avery `c1205f55-…-111205` HTTP 502; same Idempotency-Key. 22:10Z Riley: no another tag; Sam do not bounce db-east.
- Gate 1 `evidence/pipeline.log`: `Job test skipped`; `docker build -t …:3.8.9-debug -t …:latest`; `Skipping image smoke`; `register-task-definition … revision=88`; `conclusion=success`.
- Gate 2 `evidence/ecs-deployments.txt`: `ROLLBACK … ELB_HEALTH_CHECK_FAILURE`; PRIMARY `payment-service:80` / `3.8.0`; TG `PORT 8080` `PATH /actuator/health/liveness`; `(port 8080) is unhealthy`.
- Gate 3 `evidence/task-def-diff.txt`: `- SERVER_PORT 8080` / `+ SERVER_PORT 9080`; `- image …:3.8.0` / `+ …:3.8.9-debug`.

## Next investigation

(What would you open or measure next, and why? If you wanted an omitted evidence kind, say what it would show.)

After gate 1: ECS deployments (gate 2) — green CI vs PRIMARY/FAILED and TG path. After gate 2: task-def-diff (gate 3) — 88 vs 80 listen port and image. Omitted app logs: Tomcat on **9080** vs health curl **8080**. ALB access logs omitted; deployment already names 8080 unhealthy. No DB metrics — do not invent SQL. Do not invent `BAYPAY_DB_*` values.

## Stabilization action

(What restores the merchant path *now*? Last healthy task definition / image? What do you explicitly not do?)

**PRIMARY is already `payment-service:80` / `3.8.0`.** Confirm rollback completed (22:05Z) and leave it. Do **not** push `:latest` from a laptop. Do **not** register another 9080 debug tag. Do **not** retarget the ALB to 9080. Do **not** scale the service to zero (2 healthy tasks already). Do **not** bounce db-east / Postgres / `dmgr-east`. Do **not** bake secrets into a new task def. Paper only — no live `update-service` unless 80 is not PRIMARY.

## Remediation

(What remains after the page is quiet? Pipeline, tags, smoke.)

BUILD-1204: **test job** (Java 21 `./mvnw test`) + publish `needs: test`. Smoke **on 8080** (`GET /actuator/health/liveness` against the **task** listen port — localhost in CI is not enough if `SERVER_PORT` can drift). Deploy tag = **`${{ github.sha }}`**, never `:latest` or `*-debug` as the ECS image. Circuit breaker is stabilize, not a remediating control (can leave a stuck PRIMARY if rollback is off). Immutable tags so ECR can prove what 80 vs 88 was.

## Communication update

(Five lines max. Audience: merchant success + release + SRE. No unsupported cause.)

SEV-2 `pay-alb-student.baypay.example` 502/503 after BAYPAY-12051. Harbor Market / Avery `c1205f55-…-111205`; same Idempotency-Key.  
CI was **green** with **no test job and no smoke**. Image `3.8.9-debug` + `:latest` → task def **88**.  
**88** set `SERVER_PORT=9080`. TG still **8080** `/actuator/health/liveness`. Circuit breaker rolled to **`payment-service:80` / 3.8.0**.  
Merchants should be on 80 now. Not a database outage. Not retargeting the ALB to 9080.  
Jordan: no more tags until smoke on 8080 is in the pipeline. Next update when 80 stays PRIMARY and 502s stop.
