# Module 4 — Deploying on AWS with ECS Fargate

**Production-Grade Microservices on AWS · BayAreaLa8s**

| | |
|---|---|
| **Duration** | 90 minutes lecture + 4 hours lab |
| **Week** | 4 of 10 |
| **Prerequisites** | Module 3, AWS account, Terraform basics |

---

## Learning Objectives

Students will be able to:

1. Explain **ECS** components: cluster, task definition, service, task, and Fargate launch type.
2. Describe **VPC networking** for ALB, public/private subnets, NAT, and security groups.
3. Configure **ALB path-based routing** to four microservices.
4. Apply **Terraform** from `infrastructure/terraform/` with cost-control flags.
5. Deploy and verify the platform using **`aws-start.sh`**, **`aws-deploy.sh`**, and **`aws-stop.sh`**.

---

## Session Agenda

| Segment | Time | Topic |
|---------|------|--------|
| ECS & Fargate fundamentals | 25 min | Tasks, services, awsvpc |
| VPC & load balancing | 25 min | ALB, subnets, SGs |
| Terraform walkthrough | 25 min | Variables, outputs, lifecycle |
| Demo & cost control | 15 min | Start/stop scripts, verify labs |

**Diagrams:** [10-aws-deployment](../docs/diagrams/10-aws-deployment-architecture.md) · [AWS stencil VPC detail](../docs/diagrams/aws-stencils/png/10-vpc-ecs-deployment-detail.png) · [ALB routing](../docs/diagrams/aws-stencils/png/10-alb-path-routing-detail.png)

---

## 1. Amazon ECS & Fargate (25 minutes)

### 1.1 What ECS does

**Amazon Elastic Container Service (ECS)** is AWS’s container orchestrator. It schedules containers onto infrastructure you manage (EC2) or **fully managed (Fargate)**.

| Term | Definition |
|------|------------|
| **Cluster** | Logical grouping (`ms-course-dev-cluster`) |
| **Task definition** | Blueprint: image, CPU/memory, env, roles, logging |
| **Task** | Running instance of a task definition |
| **Service** | Maintains desired count of tasks, registers with load balancer |
| **Container instance** | (Fargate) abstracted—AWS runs the host |

### 1.2 Fargate vs EC2 launch type

| | Fargate | EC2 |
|---|---------|-----|
| **Server management** | None | You patch EC2 AMIs |
| **Pricing** | Per vCPU/memory per task | EC2 + ECS agent |
| **Use case** | Most microservices courses & teams | GPU, extreme cost tuning |
| **Networking** | `awsvpc` per task | `awsvpc`, bridge, host |

**Course default:** Fargate, `awsvpc`, 256 CPU / 512 MB per service (lab-sized).

### 1.3 Task definition (course)

From `infrastructure/terraform/ecs.tf`:

- **Family:** `ms-course-dev-user-service` (per service)
- **Image:** ECR URL + tag
- **Port mappings:** 8001–8004
- **Environment:** `PRODUCT_SERVICE_URL`, `EVENT_HTTP_ENDPOINT`, `JWT_SECRET`, `DYNAMODB_ORDERS_TABLE`
- **logConfiguration:** `awslogs` → CloudWatch group `/ecs/ms-course-dev`
- **healthCheck:** HTTP to `localhost:<port>/health`

### 1.4 Execution role vs task role (preview)

| Role | Used by | Permissions (course) |
|------|---------|------------------------|
| **Execution role** | ECS agent | Pull ECR, write logs |
| **Task role** | Application code | `events:PutEvents`, DynamoDB on orders table |

Deep dive in Module 7.

### 1.5 Service discovery

**AWS Cloud Map** private DNS: `product-service.ms-course-dev.local`

**Course note:** Inter-service HTTP often routes via **ALB URL** for reliability in labs (`locals.tf` sets `product_service_url` to ALB when active).

---

## 2. VPC, ALB & Security Groups (25 minutes)

### 2.1 Regional architecture

Walk the **AWS stencil diagram** (`10-vpc-ecs-deployment-detail`):

```
Internet → IGW → ALB (public subnets)
              → ECS tasks (private subnets) → NAT → Internet (egress)
```

**CIDR:** `10.0.0.0/16` VPC, public `10.0.0.0/24` & `10.0.1.0/24`, private `10.0.10.0/24` & `10.0.11.0/24`.

### 2.2 Application Load Balancer

| Feature | Course usage |
|---------|--------------|
| Listener | HTTP :80 |
| Rules | Path patterns → target groups |
| Health checks | `GET /health` on each service |
| Default action | “BayAreaLa8s Microservices Course Platform” |

**Path routing** (see `alb.tf`):

| Priority | Pattern | Target |
|----------|---------|--------|
| 10 | `/users*`, `/auth*` | user-service:8001 |
| 11 | `/products*` | product-service:8002 |
| 12 | `/orders*` | order-service:8003 |
| 13 | `/events*` | notification-service:8004 |

### 2.3 Security groups

| SG | Ingress | Purpose |
|----|---------|---------|
| **ALB** | 0.0.0.0/0:80 | Public HTTP (TLS extension: 443) |
| **ECS tasks** | From ALB + **self** (service-to-service) | Order → Product/Notification |

**Self-referencing rule:** Allows tasks in same SG to call each other on all TCP ports—needed for inter-service HTTP via ALB or direct task IPs.

### 2.4 NAT Gateway & cost

When `platform_active = true`, NAT enables **outbound** internet from private tasks (ECR pull already via VPC endpoints optional; external APIs).

When **`aws-stop.sh`:** ECS scaled to 0, NAT and ALB destroyed—saves ~$1.50–3/day.

See [`docs/AWS_COST_CONTROL.md`](../docs/AWS_COST_CONTROL.md).

---

## 3. Terraform Walkthrough (25 minutes)

### 3.1 Repository layout

```
infrastructure/terraform/
  main.tf          # Provider, backend hint
  vpc.tf           # VPC, subnets, IGW, NAT, SGs
  alb.tf           # ALB, listeners, rules
  ecs.tf           # Cluster, services, task defs, Cloud Map
  iam.tf           # Roles and policies
  variables.tf     # Inputs
  locals.tf        # platform_active, service map
  outputs.tf       # ALB DNS, etc.
```

### 3.2 Key variables

| Variable | Purpose |
|----------|---------|
| `platform_active` | `true` = ALB + NAT + running platform |
| `ecs_desired_count` | Tasks per service (0 when stopped) |
| `aws_region` | Default `us-east-1` |
| `jwt_secret` | In `terraform.tfvars` (gitignored)—use example file |

**Never commit:** `terraform.tfvars`, `*.tfstate`.

### 3.3 Apply workflow (instructor demo)

```bash
cd infrastructure/terraform
cp terraform.tfvars.example terraform.tfvars   # edit values
terraform init
terraform plan
terraform apply
```

**Or use course scripts:**

```bash
./scripts/aws-start.sh    # build, push ECR, apply active platform
./scripts/aws-stop.sh     # scale down, deactivate costly resources
./scripts/aws-deploy.sh   # rebuild amd64, force ECS deployment
```

### 3.4 Outputs students need

- `alb_dns_name` — base URL for labs
- ECR repository URLs — for manual push debugging

### 3.5 State & teamwork

- Remote state in S3 + DynamoDB lock (enterprise extension)
- Local state OK for individual learners

---

## 4. Demo, Verification & Wrap-Up (15 minutes)

### 4.1 Live verification

```bash
export ALB_URL=http://<alb-dns-name>
curl -s "$ALB_URL/products" | head
./scripts/verify-aws-labs.sh
```

### 4.2 Common failures (teaching moments)

| Symptom | Cause | Fix |
|---------|-------|-----|
| `exec format error` | arm64 image on amd64 Fargate | `docker build --platform linux/amd64` |
| 502 from ALB | Tasks unhealthy | Check `/ecs/...` logs, health path |
| Order cannot reach Product | SG or wrong URL | ALB URL in env; self-SG rule |
| ECR auth failed | Stale login | `aws ecr get-login-password` via `scripts/aws/lib.sh` |

### 4.3 Auto Scaling (concept)

**Target tracking:** Scale on CPU/memory or ALB request count per service.

Not fully exercised in base Terraform—capstone extension.

---

## Lab & Assignment

- **Lab 04:** [`labs/module-04/README.md`](../labs/module-04/README.md)
- **Assignment 04:** [`assignments/module-04.md`](../assignments/module-04.md)

### Summary

- **Fargate** removes host management; you still own **networking, IAM, and observability**.
- **ALB + path rules** replace local Compose ports in AWS.
- **Terraform + scripts** encode reproducible environments and **cost-aware** lifecycles.

---

## Discussion Questions

1. Why place ECS tasks in **private** subnets while ALB is **public**?
2. What happens to running requests during a **rolling deployment**?
3. Why does the course use path-based routing instead of one API Gateway per service?
4. How does `platform_active=false` reduce monthly cost?

---

*BayAreaLa8s · Production-Grade Microservices on AWS*
