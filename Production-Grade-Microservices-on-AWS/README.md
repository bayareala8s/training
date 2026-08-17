# Production-Grade Microservices on AWS

> **Design, Build, Deploy, Secure, Scale, and Operate Enterprise-Grade Microservices on AWS**

**Offered by [BayAreaLa8s](https://bayareala8s.com)**

| | |
|---|---|
| **Duration** | 10 weeks · 72 hours |
| **Format** | Instructor-Led / Hybrid / Self-Paced |
| **Level** | Intermediate → Advanced |

---

## Alternative Premium Titles

- Enterprise Microservices Engineering on AWS
- Cloud-Native Microservices Architecture & Operations
- Building Enterprise-Scale Microservices on AWS

---

## Target Audience

Software Engineers, Backend Developers, Cloud Engineers, DevOps Engineers, Platform Engineers, Solution Architects, senior CS students, and professionals transitioning to cloud-native development.

### Prerequisites

- Basic programming (Python, Java, or Node.js)
- Basic AWS, Linux, Git, and REST API fundamentals

---

## Course Description

Most microservices courses stop at deploying a few Docker containers. Real enterprises require service ownership, API governance, security, scalability, observability, CI/CD, disaster recovery, cost optimization, and reliability engineering.

This course teaches how enterprise teams build and operate cloud-native microservices platforms on AWS—from design through production deployment.

**Stack:** FastAPI · Spring Boot · NestJS · Docker · ECS Fargate · API Gateway · EventBridge · DynamoDB · RDS · CloudWatch · X-Ray · Terraform · GitHub Actions

---

## Learning Outcomes

By the end of this course, students will be able to:

- Design enterprise microservices architectures
- Build scalable APIs and deploy on ECS Fargate
- Implement asynchronous, event-driven systems
- Secure microservices with IAM and JWT
- Build CI/CD pipelines and implement observability and tracing
- Design resilient systems and operate production workloads

---

## Platform Architecture

**Professional diagrams (Mermaid + export guide):** [docs/diagrams/](docs/diagrams/README.md)

Includes: monolith vs microservices · context maps · C4 · sequence flows · AWS VPC/ECS · security · CI/CD · capstone

```text
                API Gateway / ALB
                       |
      ----------------------------------
      |               |                |
  User Service   Order Service   Product Service
      |               |                |
      ----------------------------------
                       |
                EventBridge
                       |
          -------------------------
          |           |           |
     Notifications Analytics Audit
                       |
                  DynamoDB
                       |
                 CloudWatch
```

---

## Syllabus

| Module | Topic | Folder |
|--------|-------|--------|
| 1 | [Microservices Foundations](modules/01-microservices-foundations/README.md) | `modules/01-microservices-foundations/` |
| 2 | [API Design & Development](modules/02-api-design-development/README.md) | `modules/02-api-design-development/` |
| 3 | [Containerization with Docker](modules/03-containerization-docker/README.md) | `modules/03-containerization-docker/` |
| 4 | [Deploying on AWS (ECS Fargate)](modules/04-deploying-on-aws/README.md) | `modules/04-deploying-on-aws/` |
| 5 | [Service-to-Service Communication](modules/05-service-communication/README.md) | `modules/05-service-communication/` |
| 6 | [Data Management & Consistency](modules/06-data-management/README.md) | `modules/06-data-management/` |
| 7 | [Security & Identity](modules/07-security-identity/README.md) | `modules/07-security-identity/` |
| 8 | [Observability & Reliability](modules/08-observability-reliability/README.md) | `modules/08-observability-reliability/` |
| 9 | [CI/CD & Production Operations](modules/09-cicd-operations/README.md) | `modules/09-cicd-operations/` |
| 10 | [Enterprise Capstone](capstone/README.md) | `capstone/` |

Full details: [docs/course-overview.md](docs/course-overview.md)

---

## Technology Tracks

| Track | Framework |
|-------|-----------|
| Python | FastAPI |
| Java | Spring Boot |
| Node.js | NestJS |

Shared labs live under `labs/`. Track-specific starters under `starters/python/`, `starters/java/`, and `starters/nodejs/`.

---

## Assessment

| Assessment | Weight |
|--------------|--------|
| Weekly Labs | 30% |
| Assignments | 20% |
| Architecture Reviews | 10% |
| CI/CD Project | 10% |
| Capstone Project | 30% |

See [docs/assessment.md](docs/assessment.md).

---

## Capstone Options

1. **E-Commerce** — User, Product, Inventory, Order, Notification
2. **Banking** — Customer, Payment, Fraud, Notification
3. **SaaS** — Authentication, Billing, User Management, Analytics

See [capstone/README.md](capstone/README.md).

---

## Teach This Course (Quick Start)

**Instructors:** Read [docs/INSTRUCTOR_GUIDE.md](docs/INSTRUCTOR_GUIDE.md) and [docs/AWS_COST_CONTROL.md](docs/AWS_COST_CONTROL.md).

```bash
# Local platform
cp .env.example .env
docker compose up --build
make test                    # all unit tests
./scripts/verify-all-labs.sh # labs 01-09 (local)

# AWS platform
./scripts/aws-start.sh       # deploy (~15-20 min first time)
./scripts/verify-aws-labs.sh # labs 04-08 on AWS
./scripts/aws-stop.sh        # stop NAT/ALB/ECS — save costs
./scripts/aws-destroy.sh     # full teardown
```

**Students:** Read [docs/STUDENT_HANDBOOK.md](docs/STUDENT_HANDBOOK.md) → start [labs/module-01/README.md](labs/module-01/README.md).

## Repository Layout

```text
.
├── README.md
├── docs/              # Instructor guide, student handbook, schedule
├── lectures/          # 90-min lecture notes (modules 1–10)
├── instructor/        # Facilitation notes per week
├── labs/module-01…09/ # Student lab workbooks
├── assignments/       # Homework prompts & rubrics
├── assessments/       # Quizzes
├── starters/python/   # Working FastAPI services (reference)
├── starters/java|nodejs/  # Track guides (implement same contracts)
├── contracts/         # OpenAPI + event schemas
├── infrastructure/terraform/
├── capstone/
└── .github/workflows/
```

---

## Career & Portfolio Outcomes

Students graduate with production deployment experience, event-driven design, CI/CD pipelines, observability dashboards, security implementation, and resume-ready GitHub repositories.

**Example resume line:**

> Designed and deployed a production-grade microservices platform on AWS using FastAPI, Docker, ECS Fargate, EventBridge, DynamoDB, CloudWatch, and GitHub Actions with automated CI/CD, distributed tracing, and event-driven communication.

---

## BayAreaLa8s Academy

Flagship offering alongside:

1. Enterprise File Transfer Automation on AWS
2. Terraform for Real Enterprises
3. AI Automation & Agents with AWS Bedrock
4. Cloud-Native Data Engineering on AWS
5. **Production-Grade Microservices on AWS** ← this course

---

## License & Usage

Course materials © BayAreaLa8s. For instructor and cohort use only unless otherwise licensed.
