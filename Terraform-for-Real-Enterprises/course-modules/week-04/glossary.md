# Week 4 — Glossary

| Term | Definition |
|------|------------|
| **GitOps** | Operational model where Git is the single source of truth for system desired state |
| **CI/CD** | Continuous integration and continuous delivery/deployment automation |
| **Pipeline gate** | Automated or manual checkpoint that must pass before proceeding (e.g. plan review) |
| **GitHub Actions** | GitHub-hosted workflow automation for build, test, and deploy |
| **Workflow** | YAML-defined automation triggered by events (push, pull_request) |
| **OIDC** | OpenID Connect; federated identity tokens used for short-lived AWS credentials |
| **AssumeRoleWithWebIdentity** | STS API assuming IAM role using OIDC/JWT from identity provider |
| **Trust policy** | IAM policy defining federated or cross-account principals allowed to assume a role |
| **GitHub Environment** | Named deployment target with protection rules and optional secrets |
| **Branch protection** | Rules requiring reviews, status checks, or blocking force-push on branches |
| **Plan job** | CI job running `terraform plan` without applying changes |
| **Apply job** | CI job running `terraform apply` after approvals |
| **Saved plan** | Binary plan file applied to ensure exact reviewed changes |
| **tflint** | Linter for Terraform with provider-specific rules |
| **Checkov** | Static analysis tool for infrastructure-as-code security policies |
| **soft_fail** | CI setting allowing job success despite tool findings (temporary/adoption pattern) |
| **Path filter** | Workflow trigger limiting runs to specific file path changes |
| **TF_VAR_** | Environment variable prefix mapping to Terraform input variables |
| **Policy-as-code** | Automated enforcement of security/compliance rules in CI |
