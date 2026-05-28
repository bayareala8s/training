# Week 3 — Enterprise Scenarios & Case Studies

## Scenario A — Global bank: unversioned modules caused production outage

**Context:** Forty application teams referenced `source = "git::...//vpc?ref=main"`. A platform engineer merged a change renaming `private_subnet_ids` output to `private_subnets`. Friday afternoon applies in twelve repos failed; one team forced an old provider and partially deployed incompatible networking.

**Impact:**

- 6-hour production networking incident in EU region
- Mandatory semver tags and CODEOWNERS on platform module repo

**Lesson:** **Pin module versions**; treat breaking output changes as MAJOR releases with migration guides.

**Discussion questions:**

1. What CI check would detect breaking output removals before tag?
2. How long should platform support N-1 major versions?

---

## Scenario B — E-commerce platform: module composition at scale

**Context:** Platform team published `vpc`, `security-group`, and `compute` modules. Product teams composed them in thin root modules per service. New PCI scope required dedicated database subnets—platform added optional `database_subnets` variable in **minor** release `v1.3.0`.

**Outcome:** Teams opted in per service; no forced Friday cutover.

**Lesson:** **Optional inputs** and minor releases enable gradual adoption across hundreds of stacks.

**Discussion questions:**

1. When does a new subnet tier require a major version bump?
2. Who owns validation rules for CIDR overlap?

---

## Scenario C — Regulated insurer: private registry governance

**Context:** Public Terraform Registry modules were banned. All sources had to resolve through `app.terraform.io/insurer/` with signed modules and RBAC. Teams attempting `github.com/community/module` were blocked at `terraform init` by network proxy.

**Pattern:**

| Control | Implementation |
|---------|----------------|
| Discovery | Private registry catalog |
| Approval | Security + architecture sign-off per module |
| Consumption | Version pins in approved wrapper templates |

**Lesson:** Module strategy includes **supply chain**—not only HCL quality.

**Discussion questions:**

1. How does private registry interact with monorepo local paths in dev?
2. What evidence do auditors request for third-party modules?

---

## Scenario D — Internal open source: README debt

**Context:** A `vpc` module had 38 undocumented variables copied from a one-off stack. New hires passed invalid CIDRs; `terraform plan` failed late Friday. Platform invested one sprint in README tables, examples/, and variable validations.

**Outcome:** Support tickets dropped 60%; module adoption increased.

**Lesson:** **Documentation is part of the API**—not stretch work.

**Discussion questions:**

1. Minimum README sections for your organization?
2. Should undocumented variables be rejected in CI?

---

## Lab tie-in

Week 3 labs extend [`modules/vpc/`](../../modules/vpc/), compose environments, and publish `v1.0.0`—see [04-hands-on-labs.md](04-hands-on-labs.md).
