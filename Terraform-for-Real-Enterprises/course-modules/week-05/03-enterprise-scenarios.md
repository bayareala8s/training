# Week 5 — Enterprise Scenarios & Case Studies

## Scenario A — Retail: Black Friday promotion skip

**Context:** A retailer promoted a cart microservice module to prod on Tuesday without applying to test first. New autoscaling settings were correct in code but **test tfvars** still referenced old `min_size`. Prod apply doubled ASG capacity during a marketing freeze.

**Impact:** $47k unexpected EC2 spend; change advisory bypassed.

**Lesson:** Promotion is a **checklist + pipeline**, not “merge to main.” Test must use the **same module version and representative tfvars** as prod.

**Discussion questions:**

1. How would saved plans have helped?
2. What CI gate would block apply when test plan artifact is missing?

---

## Scenario B — Insurance: undetected security group drift

**Context:** A network engineer opened port 22 to `0.0.0.0/0` on a bastion SG during an incident. Post-incident, Terraform was not reconciled for six weeks. Quarterly penetration test flagged critical finding.

**Impact:** Audit finding; mandatory enterprise-wide drift scan project.

**Lesson:** Drift with security impact is **incident-class**. Run `terraform plan` after break-glass; update code or revert.

**Controls:**

| Control | Role |
|---------|------|
| Nightly `terraform plan` in prod (read-only role) | Detect drift early |
| SCP deny broad SG ingress | Prevent worst case |
| Drift report template | Standardize response |

---

## Scenario C — SaaS: safe module refactor at scale

**Context:** Platform team moved `aws_instance` resources into `module.compute` for 30 service repos using `moved` blocks and a communication plan. Dev/test validated zero replacement; prod rollout took two weeks per team.

**Outcome:** No customer-facing replacements; state addresses migrated cleanly.

**Lesson:** Refactoring is a **change program**, not a single PR.

**Discussion:** When would you use `state mv` instead of `moved` blocks?

---

## Scenario D — Healthcare: environment parity failure

**Context:** Prod used RDS `db.r6g.large`; test used `db.t3.micro` due to cost. A query timeout bug reached prod because performance characteristics differed.

**Lesson:** Promotion validates **topology and config keys**, not only Terraform module version. Document acceptable skew in tfvars.

---

## Lab tie-in

Week 5 labs: promote to test ([Lab 5.1](../../labs/week-05/LAB-01-promotion.md)), simulate drift ([Lab 5.2](../../labs/week-05/LAB-02-drift.md)), remediate ([Lab 5.3](../../labs/week-05/LAB-03-remediate.md)).

See [04-hands-on-labs.md](04-hands-on-labs.md).
