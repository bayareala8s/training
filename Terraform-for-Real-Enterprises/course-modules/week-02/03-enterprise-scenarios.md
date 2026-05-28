# Week 2 — Enterprise Scenarios & Case Studies

## Scenario A — Retail conglomerate: SCP blocks production Terraform

**Context:** A platform team deploys Terraform from a shared services account into production workload accounts. After a security audit, a new SCP denies `ec2:RunInstances` unless instances use an approved AMI list. Weekend deploys fail with `AccessDenied` despite IAM policies allowing the action.

**Impact:**

- 14-hour delay for Black Friday scaling changes
- Finger-pointing between security (SCP authors) and platform (IAM authors)

**Lesson:** Terraform failures are not always IAM role bugs—**evaluate SCP inheritance** on the account and parent OUs before changing runner policies.

**Discussion questions:**

1. How would you test SCP impact before attaching to the production OU?
2. Should Terraform pipelines have a “SCP simulation” or policy-as-code check?

---

## Scenario B — Fintech: confused deputy on cross-account role

**Context:** A vendor SaaS product requested `sts:AssumeRole` into the customer’s audit account. The initial trust policy used only `Principal: AWS = vendor-account-root` without `ExternalId`. A researcher demonstrated another customer could trick the vendor into assuming the wrong customer role.

**Impact:**

- Emergency trust policy update across 200 accounts
- Mandatory `ExternalId` per customer in Terraform-generated roles

**Lesson:** Cross-account trust is a **security contract**—use `ExternalId`, narrow `PrincipalArn`, and prefer role-to-role trust over account root.

**Discussion questions:**

1. Where should `ExternalId` values be stored for Terraform-managed roles?
2. How does GitHub OIDC `sub` condition compare to `ExternalId`?

---

## Scenario C — Healthcare: landing zone vs team Terraform

**Context:** A health system deployed **AWS Control Tower** for OU structure, logging, and account vending. Application teams wanted full Terraform freedom in new accounts. Central IT mandated: landing zone resources are **read-only** to workload Terraform via SCP; only the network hub account pipeline may modify Transit Gateway attachments.

**Pattern:**

| Layer | Owner | Tooling |
|-------|-------|---------|
| Org / accounts / SCPs | Cloud foundation | Control Tower |
| Hub network | Network platform | Terraform in shared services |
| App stacks | Product teams | Terraform with approved modules |

**Lesson:** Multi-account success is **governance negotiation**, not only technical assume-role wiring.

**Discussion questions:**

1. What happens when a team `terraform import`s a landing-zone VPC?
2. Who approves exceptions to SCP deny lists?

---

## Scenario D — Startup on single account (honest lab mode)

**Context:** A 40-person startup runs dev/test/prod as tags in one account while learning enterprise patterns in this course. They document a **target** four-account design but operate single-account for 12 months.

**Outcome:** They still benefit from remote state, modules, and CI—but a compromised admin IAM user can touch all environments.

**Lesson:** Document **current state vs target state**; do not misrepresent isolation to auditors or customers.

**Discussion questions:**

1. Minimum viable step from single account to multi-account?
2. Which Week 2 artifacts still add value in single-account mode?

---

## Lab tie-in

Week 2 labs produce the architecture diagram and cross-account IAM workflow that Scenarios A–C assume—see [04-hands-on-labs.md](04-hands-on-labs.md).
