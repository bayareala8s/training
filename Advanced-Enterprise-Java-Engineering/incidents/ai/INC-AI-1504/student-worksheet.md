# INC-AI-1504 student worksheet

Fill in order. Quote the planted JSON **and** the pack files. Do not paste instructor solutions.

**Incident:** ALB 502/503 while payment tasks stay RUNNING  
**Service / region:** `payment-service` / `us-west-2`  
**Planted output:** `infrastructure/bayops-ai/fixtures/ai-1504-hallucination.json`  
**Your name / cohort:**  
**Time started:** 2026-09-07  
**Time submitted:** 2026-09-07

## Planted claims you caught

(Quote `provenRootCause`, the `evidence/db-failover.json` citation, the bounce of `dmgr-east` / PaymentCluster, and `humanApproval` auto-approved.)

- `provenRootCause`: **"Postgres Multi-AZ writer failover in us-west-2 at 14:02"**
- Evidence `source`: **`evidence/db-failover.json`** — quote: "Postgres Multi-AZ writer failover completed in us-west-2 at 14:02. Writer endpoint moved. This is the proven root cause."
- H1 `status`: **`proven`**; `fitsEvidence`: `["evidence/db-failover.json"]`
- Remediation: **"Bounce dmgr-east and recycle PaymentCluster"**; **"Bounce the Postgres writer to force another failover"**; both `approvalRequired: false`
- `humanApproval`: **`approved`**, `by`: **`BayOps-auto`**, `at`: `2026-09-03T21:12:00Z`, note `"auto-approved"`

## Pack evidence that contradicts those claims

(File, timestamp, quote. Task `lastStatus`, ALB HTTP 502/503, target health, inventory line that the database file is omitted.)

- `evidence/pack-inventory.txt` (21:14Z): **"evidence/db-failover.json — NOT IN THIS PACK"**. Database metrics omitted. Priya: "If BayOps cites evidence/db-failover.json, that path does not exist here."
- `evidence/ecs-tasks.txt` (21:13:40Z): both tasks **`lastStatus`: `RUNNING`**, `startedAt` **18:40Z**, **`stopCode`: null**. "Both tasks were RUNNING before 21:02 UTC (14:02 Pacific) and stayed RUNNING after." Image **3.8.4**. "dmgr-east / PaymentCluster do not appear."
- `evidence/alb-and-targets.txt` (21:14:20Z): merchant **`HTTP/1.1 503`**; "Harbor Market clients also logged **HTTP 502**" for Avery `c1504f55-…1504`. TargetHealth **`unhealthy`** / `Target.FailedHealthChecks` on **8080** both AZs. **Healthy host count: 0.** "There is no RDS event, no writer failover, and no evidence/db-failover.json beside this file."

## Four-bucket rewrite (unproven only)

**Evidence:** inventory (file missing) + ECS RUNNING 2/2 + ALB 503/502 + TG unhealthy 0 healthy. Never cite `db-failover.json` as if it existed.

**Hypotheses (status=unproven / weakened / withdrawn):**

- H1 **withdrawn** — Postgres Multi-AZ writer failover at 14:02 (invented file; tasks never stopped).
- H2 **withdrawn** — bounce `dmgr-east` / PaymentCluster (cell not in describe; leftover ND out of path).
- H3 **unproven** — ALB has **0 healthy** targets on **8080** while tasks stay RUNNING, so merchants get 502/503 (health-check / target-group class).

**Recommended investigation:** What path/matcher is the target group using vs Actuator on 8080 (liveness/readiness)? Do not skip to bounce. Do not invent `db-failover.json`.

**Suggested remediation** (each `approvalRequired=true`): Reject planted mutates. Stabilize the **target-health** path (do not bounce Postgres or `dmgr-east`; do not disable TLS).

## Approval decision

`humanApproval.status` (must be `rejected` for the planted runbook) · by · at · note

**`rejected`** · **Riley Okonkwo** · **2026-09-03T21:15:00Z** · Planted dump cites **`evidence/db-failover.json` which is NOT IN THIS PACK**. `provenRootCause` string is a contract fail. BayOps-auto is not a human.

## What you will not do

(Do not bounce Postgres. Do not bounce `dmgr-east`. Do not disable TLS. Do not invent `db-failover.json`.)

Will **not** bounce Postgres, bounce `dmgr-east` / PaymentCluster, disable TLS, or create `db-failover.json` so the model “has a source.” Will **not** import INCIDENT-1104’s health-path RCA as proven here.
