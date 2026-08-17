# Week 7 — Enterprise Scenarios & Case Studies

## Scenario A — Technology: leaked AWS keys in Terraform repo

**Context:** Static keys in committed `terraform.tfvars` were scraped from public GitHub within minutes. Attacker launched crypto-mining instances in a sandbox account.

**Impact:** $12k charge; mandatory OIDC migration for all CI pipelines.

**Lesson:** Secret scanning + OIDC + **no long-lived keys** in Terraform workflows.

---

## Scenario B — Energy: audit finding on missing cost tags

**Context:** Finance could not allocate $2M quarterly spend because 40% of resources lacked `CostCenter`. AWS Config rule + Terraform validations added; Checkov custom policy for tag keys.

**Outcome:** Tag compliance rose to 98% in 90 days.

**Lesson:** Tags are **financial controls**, not optional metadata.

---

## Scenario C — Government contractor: Checkov in CI blocks release

**Context:** Checkov flagged unencrypted EBS on a legacy module. Team documented risk acceptance with compensating full-disk encryption at OS level—auditor rejected without expiry date.

**Lesson:** **Documented exceptions** need tickets, owners, and review dates.

---

## Scenario D — Multi-cloud enterprise: policy layers

**Context:** SCPs denied public S3; Terraform module still allowed `acl = "public-read"` in code—plans failed at apply. Platform added Checkov policy and module fork.

**Lesson:** Align **SCP + static analysis + modules** so developers fail in PR, not prod.

---

## Lab tie-in

Week 7 labs: IAM ([Lab 7.1](../../labs/week-07/LAB-01-iam.md)), tagging ([Lab 7.2](../../labs/week-07/LAB-02-tagging.md)), compliance ([Lab 7.3](../../labs/week-07/LAB-03-compliance.md)).

See [04-hands-on-labs.md](04-hands-on-labs.md).
