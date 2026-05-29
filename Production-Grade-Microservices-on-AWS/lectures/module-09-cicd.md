# Module 9 — CI/CD, Deployment Strategies & GitOps

**Production-Grade Microservices on AWS · BayAreaLa8s**

| | |
|---|---|
| **Duration** | 90 minutes lecture + 4 hours lab |
| **Week** | 9 of 10 |
| **Prerequisites** | Modules 3–4, GitHub familiarity |

---

## Learning Objectives

Students will be able to:

1. Design a **CI/CD pipeline** from commit to ECS deployment.
2. Compare **rolling**, **blue/green**, and **canary** deployment strategies.
3. Explain **GitOps** principles and immutable artifacts.
4. Use course **GitHub Actions** workflows and `aws-deploy.sh` for releases.
5. Execute **rollback** via previous task definition revision.

---

## Session Agenda

| Segment | Time | Topic |
|---------|------|--------|
| Pipeline anatomy | 20 min | CI vs CD, stages |
| GitHub Actions & ECR | 25 min | Workflows in repo |
| Deployment strategies | 25 min | Rolling, blue/green, canary |
| Rollback & GitOps | 15 min | Revisions, desired state |
| Wrap-up | 5 min | Lab 09 |

**Diagrams:** [15-cicd-pipeline](../docs/diagrams/15-cicd-pipeline.md) · [AWS CI/CD stencil](../docs/diagrams/aws-stencils/png/15-cicd-github-ecr-ecs-detail.png)

---

## 1. CI/CD Pipeline Anatomy (20 minutes)

### 1.1 Continuous Integration (CI)

**Goal:** Every change is **built and tested** quickly.

| Stage | Purpose | Course |
|-------|---------|--------|
| **Lint** | Style, static analysis | Extension (ruff, eslint) |
| **Unit test** | Fast feedback | `pytest` per service |
| **Integration test** | API contracts | `run-all-tests.sh` |
| **Build image** | Immutable artifact | `docker build` |
| **Scan** | CVE detection | ECR scan / Trivy extension |

### 1.2 Continuous Delivery / Deployment (CD)

**Delivery:** Artifact always deployable; human approves prod.

**Deployment:** Automatic prod deploy after green CI (with guardrails).

### 1.3 Pipeline diagram

[15-cicd-pipeline](../docs/diagrams/15-cicd-pipeline.md):

```
Developer → Git push → GitHub Actions → ECR → ECS update
```

### 1.4 Principles

| Principle | Practice |
|-----------|----------|
| **Immutable artifacts** | Never patch running container—new image tag |
| **Same artifact all envs** | `sha-abc` promoted dev → staging → prod |
| **Infrastructure as code** | Terraform plan in CI |
| **Secrets from vault** | OIDC to AWS, not long-lived keys in YAML |

---

## 2. GitHub Actions & Amazon ECR (25 minutes)

### 2.1 Workflows in course repo

```
.github/workflows/
  ci-service.yml      # Test on PR
  deploy-ecs.yml      # Deploy template (configure secrets)
  README.md           # Setup instructions
```

### 2.2 Typical CI job

```yaml
# Conceptual steps
- checkout
- set up Python
- pip install -r requirements.txt
- pytest
- docker build --platform linux/amd64
- push to ECR (on main branch)
```

### 2.3 AWS authentication from GitHub

**Recommended:** OIDC federation (`aws-actions/configure-aws-credentials`)—no static `AWS_ACCESS_KEY_ID` in secrets.

**Lab fallback:** IAM user keys in GitHub Secrets (rotate regularly; not for enterprise).

### 2.4 ECR push flow

1. `aws ecr get-login-password | docker login`
2. `docker tag` with ECR URI
3. `docker push`
4. Update ECS service with new image digest

**Course script:** `./scripts/aws-deploy.sh` rebuilds amd64, pushes, forces ECS deployment.

### 2.5 Terraform in pipeline

| Job | Command |
|-----|---------|
| Plan (PR) | `terraform plan` — comment on PR |
| Apply (main) | `terraform apply -auto-approve` (protected environment) |

Coordinate **infra** changes with **app** deploys—breaking dependency order causes outages.

---

## 3. Deployment Strategies (25 minutes)

### 3.1 Rolling update (ECS default)

| Behavior | Detail |
|----------|--------|
| **Process** | Start new tasks; drain old tasks |
| **Downtime** | Minimal if health checks pass |
| **Rollback** | Previous task definition revision |
| **Risk** | Mixed versions during deploy |

**ECS settings:** `minimumHealthyPercent`, `maximumPercent`.

### 3.2 Blue/green

| Component | Role |
|-----------|------|
| **Blue** | Current production |
| **Green** | New version |
| **Switch** | ALB listener rule or target group swap |

**Pros:** Fast rollback (switch back). **Cons:** Double capacity cost during cutover.

**AWS:** CodeDeploy for ECS blue/green; ALB weighted target groups.

### 3.3 Canary

Route **5%** traffic to new version; monitor error rate; increase to 100%.

**Tools:** ALB weighted forward actions, App Mesh, feature flags.

### 3.4 Comparison table

| Strategy | Downtime | Rollback speed | Cost | Complexity |
|----------|----------|----------------|------|------------|
| Rolling | Low | Medium | Low | Low |
| Blue/green | Very low | Fast | High (2x briefly) | Medium |
| Canary | Very low | Fast | Medium | High |

**Course default:** Rolling via ECS service update.

---

## 4. Rollback & GitOps (15 minutes)

### 4.1 ECS rollback

```bash
# Identify previous task definition revision
aws ecs describe-services --cluster ms-course-dev-cluster --services order-service
aws ecs update-service --task-definition order-service:PREV_REV --force-new-deployment
```

Or re-run pipeline on previous Git tag.

### 4.2 Database migrations

**Hardest part of rollback.** Prefer **backward-compatible** migrations (expand-contract pattern):

1. Deploy code that reads old + new schema
2. Migrate data
3. Deploy code that writes new only
4. Remove old

### 4.3 GitOps (concept)

| Idea | Implementation |
|------|----------------|
| Git is desired state | Manifests in repo |
| Operator reconciles | Argo CD, Flux |
| Drift detection | Alert if manual console change |

**Fit:** Kubernetes-heavy shops; ECS teams often use Terraform + pipelines instead.

---

## Lab & Assignment

- **Lab 09:** [`labs/module-09/README.md`](../labs/module-09/README.md)
- **Assignment 09:** [`assignments/module-09.md`](../assignments/module-09.md)
- **Capstone prep:** CI/CD must be green for demo (Week 10)

### Summary

**CI** proves quality; **CD** ships safely. Choose deployment strategy based on **risk tolerance** and **observability** maturity—not hype.

---

## Discussion Questions

1. Why promote the same Docker tag digest across environments?
2. When is blue/green worth 2× capacity cost?
3. What fails if you deploy schema-breaking DB migration before new code?
4. How does GitOps differ from “run terraform apply from laptop”?

---

*BayAreaLa8s · Production-Grade Microservices on AWS*
