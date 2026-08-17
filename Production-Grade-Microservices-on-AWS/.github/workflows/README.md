# GitHub Actions — Course Examples

Example workflows for Module 9:

| Workflow | Purpose |
|----------|---------|
| `ci-service.yml` | Lint, test, build Docker image on PR |
| `deploy-ecs.yml` | Push to ECR and deploy to ECS on merge to `main` |

Copy and adapt per service. Store AWS credentials via OIDC (`aws-actions/configure-aws-credentials`) — not long-lived access keys in secrets when avoidable.
