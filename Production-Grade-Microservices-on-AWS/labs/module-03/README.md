# Lab 3 — Containerize & Push to ECR

**Duration:** 4 hours | **Module 3**

## Objectives

- Write production-style Dockerfiles (multi-stage)
- Build and run full stack with Docker Compose
- Push images to Amazon ECR

## Part A — Docker Compose (60 min)

From repo root:

```bash
cp .env.example .env
docker compose up --build
./scripts/demo-platform.sh
```

Verify all four health endpoints return `"status":"ok"`.

## Part B — Dockerfile Review (90 min)

For each service, confirm:

- Multi-stage build (builder + runtime)
- Non-root user (extension: add `USER app`)
- No secrets in image layers
- `.dockerignore` excludes `__pycache__`, `.env`

Create `.dockerignore` if missing.

## Part C — Image Optimization (45 min)

Compare image sizes:

```bash
docker images | grep -E 'user-service|product-service'
```

Document one optimization you applied (slim base image, layer caching, etc.).

## Part D — Push to ECR (90 min)

1. Apply Terraform (or create ECR repos manually)
2. Authenticate:

```bash
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <ACCOUNT>.dkr.ecr.us-east-1.amazonaws.com
```

3. Tag and push each service:

```bash
export REGISTRY=<ACCOUNT>.dkr.ecr.us-east-1.amazonaws.com/ms-course-dev
docker tag starters/python/user-service:latest $REGISTRY/user-service:latest
docker push $REGISTRY/user-service:latest
```

Repeat for product, order, notification.

## Verify your work

```bash
docker compose up -d --build
./labs/module-03/verify.sh
```

## Deliverables

- [ ] Docker Compose runs full platform locally
- [ ] Screenshots or CLI output of ECR images
- [ ] `docker-notes.md` with image sizes and optimizations

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Port in use | Change host ports in `docker-compose.yml` |
| bcrypt errors on Apple Silicon | Use provided `requirements.txt` versions |
| ECR denied | Check IAM `ecr:*` permissions |
