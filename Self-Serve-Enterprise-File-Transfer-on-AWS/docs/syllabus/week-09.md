# Week 9 — ECS Fargate large file transfers (stretch)

> **Full module content:** **[Module 9 — ECS Fargate for large file transfers](../modules/week-09-ecs-fargate.md)**

**Optional stretch** after Week 5 or the capstone. Not required for the 8-week certificate path.

## Learning objectives

- Compare **Lambda vs ECS Fargate** for long-running or large file jobs.
- Deploy an on-demand **Fargate worker** triggered by S3 (dispatcher Lambda).
- Produce an audit **manifest** (SHA-256, bytes, correlation ID) in `large/processed/`.
- Explain **RunTask on demand** cost model vs always-on MFT infrastructure.

## Topics

1. Lambda limits (timeout, `/tmp`, memory) and when to use containers  
2. Lab architecture: S3 event → dispatcher → `ecs:RunTask` → worker  
3. VPC, public subnets, S3 gateway endpoint (no NAT in lab)  
4. ECR image build (`linux/amd64` for Fargate)  
5. Step Functions `ecs:runTask.sync` (conceptual extension)  

## Lab

**Lab 9:** [../labs/lab-09-ecs-fargate-large-files.md](../labs/lab-09-ecs-fargate-large-files.md)

Terraform: `enable_ecs_worker=true` (default in lab stack).  
Scripts: `./scripts/build_ecs_worker.sh`, `./scripts/demo_ecs_large_file.sh`

## Deliverable

- Screenshot or CLI output: manifest JSON in `partners/demo/large/processed/`  
- Short architecture note (½ page): why Fargate for this prefix  

## Assessment

- **Not graded** in the standard 8-week gradebook (stretch / instructor optional).  
- May be offered as extra credit per cohort policy.

## No quiz

Use module knowledge checks in [../modules/week-09-ecs-fargate.md](../modules/week-09-ecs-fargate.md).
