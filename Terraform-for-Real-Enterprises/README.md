# Terraform for Real Enterprises (Not Toy Projects)

> **Build, Secure, Automate, and Operate Enterprise Infrastructure at Scale Using Terraform**

**Offered by [BayAreaLa8s](https://github.com/bayareala8s)** · Repository: [bayareala8s/training](https://github.com/bayareala8s/training/tree/main/Terraform-for-Real-Enterprises)

| | |
|---|---|
| **Duration** | 8 weeks · 64–72 hours |
| **Format** | Instructor-led / Hybrid / Self-paced |
| **Level** | Intermediate to Advanced |

---

## Course Description

Modern enterprises manage thousands of cloud resources across multiple AWS accounts, regions, and environments. Managing infrastructure manually is slow, error-prone, and impossible to scale.

This course teaches how real enterprises use **Terraform** to provision, automate, govern, secure, and recover infrastructure at scale—including multi-account AWS architecture, modular design, CI/CD, drift detection, rollback and disaster recovery, security guardrails, environment promotion, and cost optimization.

Unlike basic Terraform tutorials, this course focuses on **real enterprise workflows, governance, resiliency, and operational excellence**.

---

## Target Audience

- DevOps / Cloud / Platform Engineers
- Site Reliability Engineers (SREs)
- AWS Engineers & Solution Architects
- Senior CS / Cloud students
- IT professionals transitioning to infrastructure automation

### Prerequisites

- Basic AWS knowledge
- Linux fundamentals
- Git/GitHub basics
- Basic networking concepts
- Familiarity with cloud infrastructure

---

## Learning Outcomes

By the end of this course, you will be able to:

- Design enterprise-grade Terraform architectures
- Implement reusable Terraform modules
- Configure secure remote state backends
- Deploy infrastructure across multiple AWS accounts
- Build CI/CD pipelines for Terraform
- Detect and remediate infrastructure drift
- Implement rollback and recovery strategies
- Enforce security and compliance guardrails
- Deploy production-ready AWS infrastructure using Infrastructure as Code

---

## Architecture You Will Build

```text
GitHub Repository
        |
Pull Request Workflow
        |
Terraform Plan (CI Pipeline)
        |
Approval Gate
        |
Terraform Apply
        |
AWS Accounts (Dev/Test/Prod)
        |
S3 Remote State + DynamoDB Locking
        |
Monitoring / Audit / Security
```

---

## Repository Layout

```text
.
├── README.md
├── Makefile                  # bootstrap, plan, apply, lab-start/stop
├── labs/
│   ├── README.md             # Lab index
│   ├── week-01 … week-08/    # LAB-*.md step-by-step guides
│   └── shared/environments/  # dev, test, prod Terraform
├── modules/                  # vpc, compute (production-style)
├── scripts/
│   ├── aws/                  # start-lab.sh, stop-lab.sh, status-lab.sh
│   └── terraform/            # rollback-plan.sh
├── docs/                     # syllabus, assessment, runbooks
├── weeks/                    # Weekly summaries (syllabus links)
├── capstone/
├── instructor/               # INSTRUCTOR-GUIDE.md
└── .github/workflows/        # Terraform CI validation
```

## Quick start (students)

```bash
# 1. Clone and configure AWS
aws sts get-caller-identity

# 2. Week 1 — bootstrap remote state
cd labs/week-01/bootstrap
cp terraform.tfvars.example terraform.tfvars   # edit bucket name
terraform init && terraform apply

# 3. Deploy dev environment
cd ../../shared/environments/dev
cp backend.hcl.example backend.hcl
cp terraform.tfvars.example terraform.tfvars
make -C ../../../.. init ENV=dev
make -C ../../../.. apply ENV=dev

# 4. End of session — save money
make -C ../../../.. lab-stop
```

See [labs/README.md](labs/README.md) for the full lab map.

---

## Weekly Schedule

| Week | Theme | Folder |
|------|--------|--------|
| 1 | Enterprise IaC foundations | [weeks/week-01](weeks/week-01) |
| 2 | AWS multi-account architecture | [weeks/week-02](weeks/week-02) |
| 3 | Terraform modules (enterprise design) | [weeks/week-03](weeks/week-03) |
| 4 | CI/CD pipelines for Terraform | [weeks/week-04](weeks/week-04) |
| 5 | Environment promotion & drift | [weeks/week-05](weeks/week-05) |
| 6 | Rollback, recovery & DR | [weeks/week-06](weeks/week-06) |
| 7 | Security, compliance & governance | [weeks/week-07](weeks/week-07) |
| 8 | Capstone project | [capstone](capstone) |

See [docs/syllabus.md](docs/syllabus.md) for full topic lists, labs, and deliverables.

---

## Tools & Technologies

**AWS:** Organizations, IAM, S3, DynamoDB, CloudWatch, Route 53, VPC, ECS/Lambda (optional)

**DevOps:** Terraform, GitHub, GitHub Actions, Docker, AWS CLI, Python (optional)

---

## Assessment

| Component | Weight |
|-----------|--------|
| Weekly labs | 35% |
| Assignments | 15% |
| Architecture reviews | 10% |
| Final capstone | 30% |
| Participation | 10% |

Details: [docs/assessment.md](docs/assessment.md)

---

## Getting Started

1. Clone this repository.
2. Complete [weeks/week-01](weeks/week-01) — install Terraform, configure AWS, and create a remote state backend.
3. Follow each week's `README.md` and lab instructions in order.
4. Use [starter-templates](starter-templates) for recommended repo layouts.

---

## Why This Course Is Different

- Real enterprise workflows, not toy examples
- Governance, compliance, and auditability
- Disaster recovery and multi-account design
- Rollback, drift, and operational excellence
- CI/CD and GitOps for infrastructure teams

---

## BayAreaLa8s

Practical enterprise cloud training — production-grade engineering education bridging consulting and workforce development.

**Advanced tracks after completion:** Enterprise file transfer on AWS, AI automation with Bedrock, cloud-native data engineering, production microservices, enterprise reliability engineering.

---

## License

Course materials © BayAreaLa8s. See [LICENSE](LICENSE) for terms of use in cohort and enterprise training programs.
