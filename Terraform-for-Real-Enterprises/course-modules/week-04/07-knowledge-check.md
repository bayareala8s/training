# Week 4 — Knowledge Check

**Format:** 15 questions · **Time:** 20 minutes closed-book (or open-book for self-paced)

---

## Questions

1. What is the core GitOps principle for Terraform source of truth?
2. Why should `terraform apply` to production not run from unreviewed feature branches?
3. Name four CI stages commonly run before `terraform apply` in enterprises.
4. What GitHub Actions permission is required for OIDC to AWS?
5. What IAM API does GitHub Actions use with OIDC (full name)?
6. What two trust policy conditions typically restrict which GitHub workflows can assume AWS roles?
7. Why are long-lived `AWS_ACCESS_KEY_ID` secrets in GitHub discouraged?
8. What is the purpose of GitHub Environment protection rules?
9. What does `terraform fmt -check` enforce?
10. What does `terraform validate` not catch?
11. What tool does the course workflow use for security scanning on `modules/`?
12. What is `soft_fail` in Checkov CI context?
13. How can CI pass variables to Terraform without committing tfvars secrets?
14. What symptom suggests OIDC trust policy `sub` mismatch?
15. What course tag must resources keep for AWS lab cost scripts?

---

## Answer key (instructors only)

| # | Answer |
|---|--------|
| 1 | Git repository (merged code) defines desired infrastructure state |
| 2 | No peer review/plan visibility; bypasses change control and audit trail |
| 3 | Any four: fmt, validate, tflint, checkov/tfsec, plan, policy checks, cost estimation |
| 4 | `id-token: write` |
| 5 | `sts:AssumeRoleWithWebIdentity` |
| 6 | `StringEquals` on audience (`sts.amazonaws.com`) and `StringLike` on `sub` (repo/ref) — accept equivalent wording |
| 7 | Broad leakage risk, rotation burden, no scoped session, poor audit granularity |
| 8 | Require reviewers, secrets, deployment branch limits before apply jobs run |
| 9 | Canonical HCL formatting; fails CI if files would change |
| 10 | AWS permissions errors, security misconfigs, logic bugs, drift (accept reasonable examples) |
| 11 | Checkov (bridgecrewio/checkov-action) |
| 12 | Job continues despite findings—used for gradual adoption; risks if left permanent without review |
| 13 | `TF_VAR_*` environment variables, GitHub Secrets for non-Terraform secrets, Parameter Store data sources |
| 14 | `Not authorized to perform sts:AssumeRoleWithWebIdentity` / OIDC assume role failure |
| 15 | `Course=terraform-enterprise` |

**Passing score:** 80% (12/15)
