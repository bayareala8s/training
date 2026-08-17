# Week 5 — Learning Objectives

By the end of this module, students will be able to:

## Knowledge (Remember / Understand)

1. Define **environment promotion** and explain how dev, test, and prod differ in guardrails—not necessarily in code structure.
2. Describe **configuration drift** and distinguish drift from intentional configuration changes delivered through Terraform.
3. Explain the roles of `terraform plan`, refresh behavior, and optional third-party drift scanners in operations.
4. List safe refactoring techniques: `moved` blocks, `terraform state mv`, import, and when each is appropriate.

## Skills (Apply / Analyze)

5. Promote shared course modules from dev to test (and document prod steps) using separate backends, tfvars, and state keys.
6. Simulate console drift, interpret plan output, and choose remediation: revert via apply, adopt via code, or import.
7. Author an **environment promotion runbook** with approval gates aligned to Week 4 CI/CD patterns.
8. Complete a drift report using course templates with root cause and prevention controls.

## Professional practice (Evaluate / Create)

9. Recommend organizational controls that reduce prod drift (SCPs, break-glass, scheduled plan jobs).
10. Evaluate a refactoring proposal (module extraction, resource rename) for blast radius and state migration risk.

## Bloom’s alignment

| Level | Objective # |
|-------|----------------|
| Understand | 1–4 |
| Apply | 5–8 |
| Evaluate | 9–10 |

## Certification alignment (optional study)

- HashiCorp Terraform Associate: workspaces vs directories, state commands, plan output
- AWS Solutions Architect: operational excellence, deployment best practices
