# Week 4 – CI/CD Pipelines for Terraform

## Learning Objectives

- Implement GitOps-style plan on PR, apply on merge (with approval gates)
- Manage secrets safely in CI (OIDC preferred over long-lived keys)
- Validate Terraform in pipeline (fmt, validate, tflint, optional checkov)

## Topics

- GitOps workflows
- Terraform plan automation
- Approval workflows
- Secrets management
- Infrastructure validation

## Labs

| Lab | Description |
|-----|-------------|
| **4.1** | GitHub Actions: `terraform fmt`, `validate`, `plan` on pull_request |
| **4.2** | Plan → review → apply with environment protection rules |
| **4.3** | Add static analysis (tflint, checkov, or tfsec) and document failures |

## Deliverables

1. **Terraform CI/CD pipeline** — Workflow files in `.github/workflows/`
2. **Automated deployment workflow** — Documented promotion path to dev (minimum)

## Suggested Time

8–10 hours

## Lab guides

| Lab | Guide |
|-----|--------|
| 4.1 GitHub Actions | [labs/week-04/LAB-01-github-actions.md](../../labs/week-04/LAB-01-github-actions.md) |
| 4.2 Approval gates | [labs/week-04/LAB-02-approval-gates.md](../../labs/week-04/LAB-02-approval-gates.md) |
| 4.3 Validation | [labs/week-04/LAB-03-validation.md](../../labs/week-04/LAB-03-validation.md) |

Workflow template: [labs/week-04/workflows/terraform-ci.yml](../../labs/week-04/workflows/terraform-ci.yml)

## Submission

PR: `week-04: terraform ci pipeline` with screenshot or log excerpt of successful plan in CI.
