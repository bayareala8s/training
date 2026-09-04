# INC-AI-1504 student worksheet

Fill in order. Quote the planted JSON **and** the pack files. Do not paste instructor solutions.

**Incident:** ALB 502/503 while payment tasks stay RUNNING  
**Service / region:** `payment-service` / `us-west-2`  
**Planted output:** `infrastructure/bayops-ai/fixtures/ai-1504-hallucination.json`  
**Your name / cohort:**  
**Time started:**  
**Time submitted:**

## Planted claims you caught

(Quote `provenRootCause`, the `evidence/db-failover.json` citation, the bounce of `dmgr-east` / PaymentCluster, and `humanApproval` auto-approved.)

## Pack evidence that contradicts those claims

(File, timestamp, quote. Task `lastStatus`, ALB HTTP 502/503, target health, inventory line that the database file is omitted.)

## Four-bucket rewrite (unproven only)

**Evidence:**

**Hypotheses (status=unproven / weakened / withdrawn):**

**Recommended investigation:**

**Suggested remediation** (each `approvalRequired=true`):

## Approval decision

`humanApproval.status` (must be `rejected` for the planted runbook) · by · at · note

## What you will not do

(Do not bounce Postgres. Do not bounce `dmgr-east`. Do not disable TLS. Do not invent `db-failover.json`.)
