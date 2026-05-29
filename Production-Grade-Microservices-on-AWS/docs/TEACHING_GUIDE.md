# Teaching Guide — Setup & Delivery

## Instructor Setup (30 minutes)

### 1. Local environment

```bash
# Prerequisites: Docker, Python 3.12+, AWS CLI v2, Terraform 1.5+
cp .env.example .env
docker compose up --build
```

Verify health:

```bash
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
curl http://localhost:8004/health
```

### 2. AWS cohort environment

```bash
cd infrastructure/terraform
cp terraform.tfvars.example terraform.tfvars
# Edit: project_name, aws_region, environment
terraform init
terraform plan
# terraform apply  # when ready for Module 4+
```

### 3. Student repositories

**Option A — Monorepo (simplest):** Students fork this repo.  
**Option B — Per-service repos:** Use template repos per service (advanced cohorts).

### 4. GitHub Classroom (optional)

- One assignment per module linking to lab README
- Autograding optional; manual review for architecture modules

## Student Setup (15 minutes)

Share with students:

1. Install Docker Desktop, Python 3.12, Git
2. Clone repo, copy `.env.example` to `.env`
3. `docker compose up --build`
4. Open `docs/STUDENT_HANDBOOK.md`

## Delivery Tips

- **Week 1:** Emphasize bounded contexts; avoid premature Kubernetes discussions.
- **Week 4:** Do AWS deploy as live demo; students follow lab asynchronously if timeboxed.
- **Week 5:** Draw event flows on whiteboard before opening EventBridge console.
- **Week 7:** Run a “threat modeling” breakout (15 min) on the order flow.
- **Week 10:** Demo day — strict 20-minute slots.

## Hardware / Cloud Budget

| Resource | Est. monthly (10 students, shared dev) |
|----------|----------------------------------------|
| ECS Fargate (2 tasks × 3 services) | $50–120 |
| DynamoDB on-demand | $5–25 |
| NAT Gateway | $35–45 per AZ |
| **Tip** | Use single NAT, destroy sandboxes nightly |

## License

BayAreaLa8s course materials — instructor use for enrolled cohorts.
