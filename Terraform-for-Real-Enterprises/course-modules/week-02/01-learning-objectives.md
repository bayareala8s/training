# Week 2 — Learning Objectives

By the end of this module, students will be able to:

## Knowledge (Remember / Understand)

1. Explain why enterprises use multiple AWS accounts instead of a single account with many VPCs.
2. Describe AWS Organizations components: management account, member accounts, OUs, and consolidated billing.
3. Define service control policies (SCPs) and how they differ from IAM policies.
4. Articulate the purpose of a landing zone (account vending, guardrails, baseline networking).
5. Identify where shared services (DNS, egress, CI, centralized logging) typically live in a multi-account model.

## Skills (Apply / Analyze)

6. Design an OU/account layout for dev, test, prod, security, and shared services with a state-backend mapping table.
7. Author and interpret cross-account IAM trust policies and least-privilege permission policies for a Terraform runner role.
8. Configure or document AWS provider `assume_role` for workload account operations.
9. Execute `terraform plan` using temporary credentials from `sts assume-role` (or equivalent SSO role chain).
10. Map Terraform state file keys to account boundaries and explain blast-radius implications.

## Professional practice (Evaluate / Create)

11. Evaluate trade-offs between single-account lab mode and true multi-account production patterns.
12. Produce architecture documentation suitable for a platform engineering review (diagram + account matrix + IAM narrative).

## Bloom’s alignment

| Level | Objective # |
|-------|----------------|
| Understand | 1–5 |
| Apply | 6–9 |
| Evaluate | 10–12 |

## Certification alignment (optional study)

- AWS Solutions Architect: design multi-account strategies, IAM cross-account access
- HashiCorp Terraform Associate: provider configuration, workspaces (contrast with accounts)
