# Module 9 Lecture — CI/CD & Operations

## Pipeline Stages

1. Lint / test
2. Build image
3. Scan (optional)
4. Push ECR
5. Deploy ECS

## Deployment Strategies

- **Rolling** — gradual task replacement
- **Blue/Green** — two environments, switch traffic
- **Canary** — small % traffic first

## GitOps Concept

Git as source of truth; pipeline reconciles desired state.

## Rollback

Previous task definition revision + forced deployment.

## Lab

`labs/module-09/README.md`
