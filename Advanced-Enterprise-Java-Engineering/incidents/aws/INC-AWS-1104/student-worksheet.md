# INC-AWS-1104 student worksheet

Fill in order. Quote evidence. Do not paste instructor solutions.

**Incident:** ALB 502/503 while payment tasks stay RUNNING  
**Region:** `us-west-2`  
**Cluster / service:** `baypay-1101-cluster` / `baypay-1101-payment`  
**Your name / cohort:**  
**Time started:** 2026-09-06  
**Time submitted:** 2026-09-06  

## Current hypothesis

(What do you think is happening? Update after each gate.)

Gate 1: Target `10.20.1.47:8080` **unhealthy** (`Target.FailedHealthChecks`, codes **[404]**). Same on `10.20.2.18`. Health check HTTP **8080** path **`/`**, matcher **200**. A **404** means the packet **arrived** — not `Target.Timeout`, not an SG miss, not “open 8080 to the world.” Sam (BAYPAY-11041) used the BUILD-1101 starter default path. Spring Boot has no index on `/` (ACCOUNT.md / BUILD-305: liveness is `/actuator/health/liveness`). Same *class* as INC-1003 (wrong probe URL), different object (ALB TG, not kubelet). Next: task-def — confirm `lastStatus` RUNNING and `containerPort` 8080 so this is not a crashed JVM. Then listener/curl only to confirm edge 502/503 when healthy=0.

Gate 2: Task `c1104task…` **`lastStatus: RUNNING`** since 21:22Z; container `payment` RUNNING; `containerPort` **8080**; image `3.9.2`; `exitCode` null; ECS `healthStatus: UNKNOWN` (no ECS-native healthCheck — ALB TG is the health object). Process is up; IP `10.20.1.47` matches the unhealthy target. Not CrashLoop, not OOM, not a missing port. Question for gate 3: does listener/curl of `pay-alb-student.baypay.example` return **502/503** from the **edge** (no healthy target) rather than a Spring 404/500 or a TLS failure? If yes, do not widen SG and do not bounce a database that is not in this estate.

Gate 3: Yes. Listener `:80` forwards to `baypay-1101-tg`. Curl **HTTP 503** from the **ALB** (`X-Request-Id: c1104-alb-503-001`). `/api/v1/payments` and even `/actuator/health/liveness` **through the ALB** are 503 — Avery never reached a healthy target. TCP to the ALB completed; not TLS (HTTP :80). RCA: target group path **`/`** 404s; matcher wants 200; TG unhealthy; merchants 502/503. Task stays RUNNING.

## Supporting evidence

(File, timestamp, quote. Target state, health-check path, health-check port, HTTP code or reason, task lastStatus, listener HTTP.)

- `timeline.json` 21:20Z Sam: registered 3.9.2 + BUILD-1101 starter TG (BAYPAY-11041); tasks RUNNING; health check “uses the default path.” 21:55Z Priya: RUNNING, TG unhealthy; describe-target-health before blaming SG. 22:10Z pager 502/503. 22:11Z Avery `c1104c44-…-111104` HTTP 503; same Idempotency-Key; some 502. 22:13Z Riley: do not open 8080 to `0.0.0.0/0` when a reason code exists.
- Gate 1 `evidence/target-health.txt` 22:14Z: `Health checks failed with these codes: [404]`; `HealthCheckPath: "/"`; port 8080; matcher 200; Healthy 0.
- Gate 2 `evidence/task-def.json` 22:16Z: `lastStatus: RUNNING`; `containerPort: 8080`; IP `10.20.1.47`; `healthStatus: UNKNOWN`.
- Gate 3 `evidence/alb-listener.txt` 22:18Z: forward to same TG; `HTTP/1.1 503`; liveness via ALB also 503.

## Next investigation

(What would you open or measure next, and why? If you wanted an omitted evidence kind, say what it would show.)

After gate 1: task-def (gate 2) — RUNNING + 8080 vs crashed/wrong port. After gate 2: listener/curl (gate 3) — unhealthy TG should be edge 502/503. Omitted SG describe: a **timeout** / `Target.Timeout` would support SG/wrong port; this pack has **HTTP 404**. Omitted app logs: GET `/` → 404 vs GET `/actuator/health/liveness` → 200 on the task IP. No RDS in this estate. Do not invent flow-log numbers.

## Stabilization action

(What restores healthy targets *now*? Path versus image versus security group? What do you explicitly not do?)

Set target-group `health_check.path` to **`/actuator/health/liveness`** (port 8080, matcher **200**). Do **not** add a controller that serves `/`. Do **not** add `404` to the matcher. Do **not** widen 8080 to `0.0.0.0/0`. Do **not** restart the RUNNING task as the fix. Do **not** bounce RDS / `dmgr-east`. Do **not** delete the ALB. Do **not** attach admin IAM to debug. Paper change (same as BUILD-1101 `work/`).

## Remediation

(What remains after the page is quiet? Terraform module?)

Bake `health_check.path = "/actuator/health/liveness"` into the Terraform module (BUILD-1101 work tree). **CI / policy must fail** when path is `/` (provider default). App repo owns Actuator groups; platform module owns the TG path — same contract as INC-1003. `/` is a reliability smell: Spring has no index. Matcher accepting 404 “so the ALB goes green” hides a wrong URL forever. Avery’s 502/503 retries / same Idempotency-Key are correct.

## Communication update

(Five lines max. Audience: merchant success + platform lead. No unsupported cause.)

SEV-2 `pay-alb-student.baypay.example` HTTP **502/503**. Harbor Market / Avery `c1104c44-…-111104`; same Idempotency-Key.  
Fargate task **RUNNING** (`3.9.2`, port 8080). Not a crashed JVM.  
Target group `baypay-1101-tg`: health path **`/`** returns **404**; matcher 200 → unhealthy. Packet arrived — not an SG timeout.  
Sam’s BAYPAY-11041 used the starter default path. Setting path to `/actuator/health/liveness`. Not opening 8080 to the world.  
No student RDS. Next update when healthy targets = 1 and curl of `/api/v1/payments` is not 503.
