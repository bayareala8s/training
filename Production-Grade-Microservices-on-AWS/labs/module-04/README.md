# Lab 4 — Deploy to ECS Fargate

**Duration:** 4 hours | **Module 4**

## Objectives

- Provision infrastructure with Terraform
- Deploy containerized services to ECS Fargate
- Configure load balancer health checks

## Part A — Terraform Apply (45 min)

```bash
cd infrastructure/terraform
terraform init && terraform apply
terraform output
```

Record: `ecs_cluster_name`, `ecr_repository_urls`, `vpc_id`.

## Part B — ECS Task Definition (90 min)

Create `infrastructure/ecs/task-definition-user.json` (template below) with:

- Fargate compatibility
- awsvpc network mode
- CloudWatch logs to `/ecs/ms-course-dev`
- Environment: `DATABASE_URL`, `JWT_SECRET` from Secrets Manager (Week 7)

**Minimal task definition fields:**

- `family`, `cpu`, `memory`, `executionRoleArn`
- Container: image from ECR, port 8001, health check `GET /health`

## Part C — ECS Service (90 min)

- Create service in private subnets
- Attach to Application Load Balancer (instructor may provide ALB Terraform extension)
- Desired count: 1 (dev)

## Part D — Auto Scaling (45 min)

Define target tracking on CPU (target 70%) for order-service.

Document scaling policy in `docs/your-name/ecs-scaling.md`.

## Verify your work

```bash
./scripts/aws-start.sh          # start AWS (first time ~15 min)
./labs/module-04/verify.sh      # checks ECS + ALB
```

## Deliverables

- [ ] At least **user-service** and **product-service** running on ECS
- [ ] ALB URL returns `/health` = ok
- [ ] Architecture diagram updated with AWS components

## Instructor Demo URL

Share ALB DNS with class; students curl `/health` through load balancer.
