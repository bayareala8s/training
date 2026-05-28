# Week 1 — Enterprise Scenarios & Case Studies

## Scenario A — Financial services: audit failure from local state

**Context:** A regional bank’s DevOps team stored Terraform state on individual laptops. An engineer left the company; their laptop was wiped. State for production VPC was lost.

**Impact:**

- Terraform proposed recreating VPC (would change CIDR routing and break compliance zone separation)
- 72-hour change freeze while network team manually reconciled AWS console vs documentation

**Lesson:** Remote state with versioning, locking, and IAM restrictions is not optional for regulated industries.

**Discussion questions:**

1. Who should have IAM access to the state bucket?
2. How would S3 versioning have helped recovery?

---

## Scenario B — SaaS startup: velocity with guardrails

**Context:** A Series B SaaS company moved from click-ops to Terraform. They adopted:

- S3 backend from day one
- `default_tags` for `Environment`, `Team`, `CostCenter`
- PR-required `terraform plan` output

**Outcome:** Environment spin-up dropped from 3 days to 4 hours; finance gained cost reports by tag.

**Lesson:** Early investment in state and tags pays off before multi-account complexity.

---

## Scenario C — Healthcare: HIPAA and change traceability

**Context:** A health-tech platform must prove **who** changed **what** in infrastructure supporting PHI workloads.

**Controls mapped to Week 1:**

| HIPAA expectation | Terraform practice |
|-------------------|-------------------|
| Access control | IAM roles for CI, no shared users |
| Audit trails | Git history + CI logs + CloudTrail |
| Integrity | State locking, PR reviews |

**Lesson:** Terraform is evidence generation—not just provisioning.

---

## Scenario D — Enterprise IT: CloudFormation coexistence

**Context:** Central IT mandates CloudFormation Service Catalog for guardrails; application teams want Terraform for microservices AWS resources.

**Pattern:**

- Landing zone (OU, SCPs) — CloudFormation / Control Tower
- Application stacks — Terraform with approved modules only

**Lesson:** Tool choice is organizational politics plus technical fit—learn both narratives.

---

## Lab tie-in

Week 1 labs simulate Scenario B’s foundation: remote state, tags, baseline VPC/compute in dev.

See [04-hands-on-labs.md](04-hands-on-labs.md).
