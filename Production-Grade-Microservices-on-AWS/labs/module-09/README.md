# Lab 9 — CI/CD Pipeline

**Duration:** 4 hours | **Module 9**

## Objectives

- Build GitHub Actions workflow: test → build → push ECR → deploy ECS
- Implement rolling deployment
- Document rollback procedure

## Part A — CI on Pull Request (90 min)

Copy `.github/workflows/ci-service.yml` to per-service workflows or use matrix strategy.

Requirements:

- Run `pytest` on Python services
- Build Docker image
- Fail PR if tests fail

## Part B — CD on Merge (90 min)

Create `.github/workflows/deploy-ecs.yml`:

1. Trigger on `push` to `main`
2. Configure AWS credentials (OIDC recommended)
3. Push image to ECR
4. Update ECS service force new deployment

## Part C — Deployment Strategies (45 min)

Document in `docs/your-name/deployment-strategies.md`:

| Strategy | Pros | Cons | When to use |
|----------|------|------|-------------|
| Rolling | | | |
| Blue/Green | | | |
| Canary | | | |

## Part D — Rollback Runbook (45 min)

Write steps to rollback a bad deploy in < 15 minutes.

## Verify your work

```bash
./scripts/run-all-tests.sh
./labs/module-09/verify.sh
```

## Deliverables

- [ ] Green CI on sample PR
- [ ] Successful deploy workflow run (screenshot)
- [ ] Rollback runbook

## GitHub OIDC Setup

See [AWS docs](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services).
