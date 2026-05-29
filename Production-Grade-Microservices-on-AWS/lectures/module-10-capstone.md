# Module 10 — Capstone Kickoff & Production Demo

**Production-Grade Microservices on AWS · BayAreaLa8s**

| | |
|---|---|
| **Duration** | 2 hours kickoff lecture + 8 hours studio + demo day |
| **Week** | 10 of 10 |
| **Prerequisites** | Modules 1–9 complete |

---

## Learning Objectives

Students will be able to:

1. Select and scope a **capstone domain** (E-Commerce default, Banking, or SaaS).
2. Produce architecture artifacts meeting [`capstone/rubrics.md`](../capstone/rubrics.md).
3. Deliver a **15–20 minute live demo** on AWS with events, security, observability, and CI/CD.
4. Present **cost and operations** awareness (start/stop, SLO summary).

---

## Session Agenda (Kickoff — 2 hours)

| Segment | Time | Topic |
|---------|------|--------|
| Expectations & rubric | 30 min | Grading criteria walkthrough |
| Domain options | 20 min | E-Commerce, Banking, SaaS |
| Architecture standards | 30 min | Min services, diagrams, contracts |
| Timeline & milestones | 20 min | Day-by-day plan |
| Team logistics & Q&A | 20 min | Teams, office hours, AWS budget |

**Diagrams:** [16-capstone-ecommerce](../docs/diagrams/16-capstone-ecommerce.md) · [17-aws-cost-lifecycle](../docs/diagrams/17-aws-cost-lifecycle.md)

---

## 1. Capstone Expectations (30 minutes)

### 1.1 Minimum technical bar

| Requirement | Evidence |
|-------------|----------|
| **≥ 3 microservices** deployed on **ECS Fargate** | Live URLs via ALB |
| **API contracts** | OpenAPI in repo |
| **Event-driven flow** | At least one async event (e.g. order → notification) |
| **Database-per-service** | No shared DB across services |
| **Security** | JWT or equivalent; IAM task roles; private tasks |
| **Observability** | CloudWatch logs + one dashboard or alarm |
| **CI/CD** | Green pipeline to ECR/ECS |
| **IaC** | Terraform (can extend course modules) |

### 1.2 Deliverables

| Artifact | Format |
|----------|--------|
| Architecture diagram | C4 context + container; AWS stencil encouraged |
| API & event contracts | `contracts/` directory |
| Runbook (1 page) | Deploy, rollback, on-call steps |
| Cost estimate | Monthly AWS rough cut |
| Demo video or live demo | 15–20 minutes |

**Full rubric:** [`capstone/rubrics.md`](../capstone/rubrics.md)  
**Templates:** [`capstone/templates/`](../capstone/templates/)

### 1.3 What excellent looks like

- Clear **bounded contexts** and context map
- **Idempotent** event consumer
- **Structured logs** with correlation id
- **SLO** stated for one critical path
- **Rollback** demonstrated or documented
- Honest **trade-offs** section in README

### 1.4 What fails capstone

- Monolith in disguise (shared database, synchronous-only spaghetti)
- No AWS deployment (local only)
- Secrets in Git
- Cannot explain architecture in Q&A

---

## 2. Domain Options (20 minutes)

### 2.1 Option A — E-Commerce (default)

**Reference:** Course platform (User, Product, Order, Notification).

**Extensions:**

- Payment service (mock Stripe)
- Inventory reservation saga
- Admin catalog CRUD with JWT roles

**Diagram:** [16-capstone-ecommerce](../docs/diagrams/16-capstone-ecommerce.md)

### 2.2 Option B — Banking / FinTech

| Service ideas | Notes |
|---------------|-------|
| Account | KYC placeholder |
| Transfer | Double-entry ledger in one service |
| Notification | Fraud alert events |
| Audit | Append-only event log |

**Constraints:** Strong audit, no float errors (`Decimal`), discuss PCI scope (out of band for real cards).

### 2.3 Option C — SaaS B2B

| Service ideas | Notes |
|---------------|-------|
| Tenant | Multi-tenancy key on all rows |
| Subscription | Plan limits |
| Usage | Metering events to billing |
| Email | Invitation workflow |

**Focus:** Tenant isolation in data model and auth claims.

### 2.4 Scoping advice

| Team size | Recommended scope |
|-----------|-------------------|
| Solo | Extend course 4 services + 1 new capability |
| Pair | 4–5 services + saga or payment |
| Team of 4 | 5–6 services max—operational overhead grows fast |

---

## 3. Architecture Standards (30 minutes)

### 3.1 Required diagrams

1. **C4 System Context** — users and externals
2. **C4 Container** — services, ALB, EventBridge, data stores
3. **AWS deployment** — VPC, subnets, ECS (use [aws-stencils](../docs/diagrams/aws-stencils/README.md))

### 3.2 Contract-first

All HTTP APIs documented in OpenAPI **before** sprint coding.

Events use JSON Schema in `contracts/events/`.

### 3.3 Operational readiness

Students must run:

```bash
./scripts/aws-start.sh    # before demo week
./scripts/aws-stop.sh     # after demo to save cost
```

**Cost diagram:** [17-aws-cost-lifecycle](../docs/diagrams/17-aws-cost-lifecycle.md)

### 3.4 Repository structure

```
team-capstone/
  contracts/
  infrastructure/terraform/
  services/<name>/
  .github/workflows/
  README.md              # how to run, arch decisions
  docs/architecture.png
```

---

## 4. Timeline & Milestones (20 minutes)

### Suggested 5-day studio schedule

| Day | Milestone | Exit criteria |
|-----|-----------|---------------|
| **1** | Architecture approved | Context map signed by instructor/peer |
| **2** | Core APIs + local Compose | Happy path demo local |
| **3** | AWS deploy + events | ALB works; event visible in logs |
| **4** | Security + observability | JWT, alarms/dashboard, CI green |
| **5** | Rehearsal | Dry-run demo under 20 min |

### Demo day format (15–20 min per team)

| Segment | Time |
|---------|------|
| Architecture & trade-offs | 3 min |
| Live happy path | 8 min |
| Failure or observability story | 3 min |
| CI/CD + cost | 3 min |
| Q&A | 3 min |

### Instructor office hours

Focus on **boundary disputes** (“should payment be in Order?”) and **ops blockers** (ECR, SG, health checks).

---

## 5. Team Logistics & Q&A (20 minutes)

### AWS account policy

- Use course AWS account or student account with **billing alert**
- **Tag** resources `Project=capstone`, `Team=<name>`
- Run `aws-stop.sh` when not testing

### Academic integrity

- Contracts may reference course repo with attribution
- Code must be team-authored; no copy-paste of full solutions from external repos

### Grading overview

| Category | Weight (typical) |
|----------|------------------|
| Architecture & design | 25% |
| Implementation & demo | 35% |
| Security & operations | 20% |
| CI/CD & IaC | 10% |
| Documentation & communication | 10% |

See rubric for exact points.

---

## Resources

| Resource | Link |
|----------|------|
| Capstone README | [`capstone/README.md`](../capstone/README.md) |
| Cost template | [`capstone/templates/cost-analysis-template.md`](../capstone/templates/cost-analysis-template.md) |
| Diagram guide | [`capstone/templates/architecture-diagram-guide.md`](../capstone/templates/architecture-diagram-guide.md) |
| Course index | [`docs/COURSE_INDEX.md`](../docs/COURSE_INDEX.md) |

---

## Closing Message to Cohort

> “Production-grade is not more microservices—it is **clear boundaries**, **automated delivery**, **observable** behavior, and **honest** operations. Your capstone proves you can ship and support a system, not just code a demo.”

---

*BayAreaLa8s · Production-Grade Microservices on AWS*
