# Week 1 — Learning Objectives

By the end of this module, students will be able to:

## Knowledge (Remember / Understand)

1. Define Infrastructure as Code (IaC) and explain its role in enterprise cloud operating models.
2. Compare Terraform and AWS CloudFormation across dimensions: ecosystem, state, multi-cloud, team workflows, and governance.
3. Describe the Terraform workflow: `init` → `plan` → `apply` → `destroy` and what each phase does internally.
4. Explain the purpose of Terraform state, why it must be protected, and risks of local-only state in teams.

## Skills (Apply / Analyze)

5. Install and verify Terraform, AWS CLI, and Git on a workstation suitable for enterprise labs.
6. Configure the AWS provider with version constraints, regions, profiles/SSO, and `default_tags`.
7. Bootstrap an encrypted S3 backend with versioning, public access blocked, and DynamoDB state locking.
8. Organize a repository using environment directories, modules, and bootstrap separation.

## Professional practice (Evaluate / Create)

9. Articulate three enterprise IaC failure modes (state corruption, untracked drift, secret leakage) and mitigations.
10. Document a baseline infrastructure deployment suitable for handoff to a platform engineering team.

## Bloom’s alignment

| Level | Objective # |
|-------|----------------|
| Understand | 1–4 |
| Apply | 5–8 |
| Evaluate | 9–10 |

## Certification alignment (optional study)

- AWS Solutions Architect: design resilient/decoupled architectures (foundation)
- HashiCorp Terraform Associate: IaC concepts, CLI workflow, state basics
