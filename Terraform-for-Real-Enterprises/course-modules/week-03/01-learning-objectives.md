# Week 3 — Learning Objectives

By the end of this module, students will be able to:

## Knowledge (Remember / Understand)

1. Explain the difference between root modules and child modules in Terraform.
2. Describe how module inputs, outputs, and `source` arguments form a published contract.
3. Define semantic versioning (MAJOR.MINOR.PATCH) as applied to Terraform module releases.
4. Compare module source types: local path, Git URL, and private Terraform Registry.
5. Articulate why pinning `ref=` to a tag—not `main`—is required in production.

## Skills (Apply / Analyze)

6. Design input variables with types, descriptions, and validations for a reusable VPC module.
7. Export outputs that enable composition with downstream modules (e.g. subnet IDs → compute).
8. Trace data flow from `module.vpc` outputs to `module.compute` inputs in environment stacks.
9. Extend an existing module with a backward-compatible optional feature and document it in README.
10. Create a Git tag release and CHANGELOG entry following team versioning policy.
11. Run `terraform fmt`, `validate`, and `make validate` across dev/test/prod configurations.

## Professional practice (Evaluate / Create)

12. Critique a “god module” anti-pattern and propose a decomposition into composable modules.
13. Write an upgrade guide for consumers moving from one major module version to the next.

## Bloom’s alignment

| Level | Objective # |
|-------|----------------|
| Understand | 1–5 |
| Apply | 6–11 |
| Evaluate | 12–13 |

## Certification alignment (optional study)

- HashiCorp Terraform Associate: modules, module sources, versioning concepts
- Platform engineering interviews: module API design, registry governance
