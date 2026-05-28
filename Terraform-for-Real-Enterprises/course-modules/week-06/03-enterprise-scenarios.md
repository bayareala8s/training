# Week 6 — Enterprise Scenarios & Case Studies

## Scenario A — Fintech: failed apply during market hours

**Context:** A partial apply created a new ALB target group but failed attaching listeners. Traffic routing was inconsistent for 12 minutes until forward fix applied.

**Impact:** SEV-2 incident; post-mortem required state snapshot and plan archive.

**Lesson:** Run applies outside peak when possible; use **small blast-radius stacks** so failures are isolated.

**Discussion:** What would `terraform state list` show mid-incident?

---

## Scenario B — Media: state bucket accidental delete attempt

**Context:** A junior engineer ran a cleanup script targeting the wrong prefix. S3 versioning and MFA delete on the state bucket prevented data loss; operations restored prior version in 20 minutes.

**Impact:** No customer outage; IAM policy updated to deny `s3:DeleteObject` on state prefix except break-glass role.

**Lesson:** **State bucket is crown jewels**—versioning, replication, SCPs.

---

## Scenario C — E-commerce: Git revert rollback

**Context:** A bad module bump increased NAT gateway count in prod. Team reverted Git commit, CI ran plan showing destroys/creates, applied during window with approval.

**Outcome:** Service restored in 45 minutes; forward fix shipped next sprint with test coverage.

**Lesson:** Git revert is standard **if state matches AWS**; otherwise reconcile first.

---

## Scenario D — Global bank: regional outage tabletop

**Context:** Primary region unavailable; DR runbook assumed manual DNS failover. Terraform state for secondary region was current; apply had been tested monthly.

**Outcome:** Tabletop revealed missing runbook step for **DynamoDB lock table** in secondary—updated Week 6 assignment template.

**Lesson:** DR is Terraform + DNS + data plane + **runbooks**, not apply alone.

---

## Lab tie-in

Week 6 labs: failed deploy ([Lab 6.1](../../labs/week-06/LAB-01-failed-deploy.md)), state recovery ([Lab 6.2](../../labs/week-06/LAB-02-state-recovery.md)), rollback ([Lab 6.3](../../labs/week-06/LAB-03-rollback.md)).

See [04-hands-on-labs.md](04-hands-on-labs.md).
