# Week 4 — Learning Objectives

By the end of this module, students will be able to:

## Knowledge (Remember / Understand)

1. Explain GitOps principles as applied to Terraform (Git as source of truth, PR plans, gated applies).
2. Describe the separation of `terraform plan` on pull requests vs `terraform apply` on protected branches.
3. Articulate why long-lived AWS access keys in GitHub Secrets are an anti-pattern for production.
4. Define OIDC federation between GitHub Actions and AWS IAM (`AssumeRoleWithWebIdentity`).
5. List standard CI stages for Terraform: fmt, validate, security scan, plan, apply.

## Skills (Apply / Analyze)

6. Configure a GitHub Actions workflow from the course template for fmt, validate, and plan on PR.
7. Set up or document IAM OIDC provider and `github-terraform` role trust policy with `sub` conditions.
8. Configure GitHub Environment protection rules requiring reviewers before apply.
9. Integrate Checkov (or similar) into CI and document findings with fix or accepted-risk rationale.
10. Use `TF_VAR_*` environment variables in CI instead of committing secrets in tfvars.
11. Interpret common CI failures: OIDC trust mismatch, state lock, backend init, AccessDenied.

## Professional practice (Evaluate / Create)

12. Design a pipeline diagram for dev vs prod accounts with separate roles and approval counts.
13. Recommend hard-fail vs soft-fail policy for security scanners based on organizational maturity.

## Bloom’s alignment

| Level | Objective # |
|-------|----------------|
| Understand | 1–5 |
| Apply | 6–11 |
| Evaluate | 12–13 |

## Certification alignment (optional study)

- HashiCorp Terraform Associate: automation concepts, workflow
- AWS: IAM OIDC identity providers, least privilege for CI roles
