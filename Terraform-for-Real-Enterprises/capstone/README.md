# Week 8 – Capstone Project

Choose **one** option. All options require production-style practices from weeks 1–7.

---

## Option 1 – Enterprise Landing Zone

Deploy secure multi-account AWS foundation infrastructure.

**Must include:**

- OU/account model (design doc)
- Shared networking or security baseline (VPC, flow logs, or equivalent)
- Remote state per account or environment
- CI/CD with plan on PR

---

## Option 2 – Shared Services Platform

Build centralized networking and monitoring platform.

**Must include:**

- Hub VPC or transit-style design (simplified acceptable for cohort)
- Centralized logging or monitoring (CloudWatch, flow logs)
- Consumable outputs for spoke/workload accounts (subnets, TGW attachment pattern, or documented interface)

---

## Option 3 – Multi-Region DR Infrastructure

Create disaster recovery–enabled infrastructure deployment.

**Must include:**

- Primary and secondary region resources (or active-passive design)
- State and config strategy for failover
- Runbook for failover / failback (tabletop acceptable)

---

## Option 4 – Internal Terraform Platform

Build reusable Terraform platform for internal teams.

**Must include:**

- Module library (≥2 modules) with versioning
- Golden path documentation for service teams
- CI template or workflow reusable by consumers

---

## Required Capstone Deliverables

| Deliverable | Description |
|-------------|-------------|
| Terraform repositories | Clean layout, remote state, modules where appropriate |
| CI/CD pipelines | Plan/apply with validation and approval |
| Architecture diagrams | Logical + network (or equivalent) |
| Cost analysis | Rough monthly estimate or cost allocation tags |
| Security review | IAM, encryption, public exposure, secrets handling |
| Final presentation | Demo + Q&A (15–20 min) |

---

## Evaluation Rubric (30% of course grade)

| Criterion | Excellent (4) | Proficient (3) | Needs work (2) |
|-----------|---------------|----------------|----------------|
| **Architecture** | Clear multi-account/env design, justified tradeoffs | Sound design, minor gaps | Unclear boundaries or single-account toy layout |
| **Terraform quality** | Modular, versioned, documented | Works, some duplication | Monolithic, hard to maintain |
| **CI/CD & ops** | Full PR workflow, drift/rollback considered | Plan/apply automated | Manual only |
| **Security** | Least privilege, no secrets in Git, guardrails | Mostly secure | Critical gaps |
| **Docs & demo** | Runbooks, diagrams, confident demo | Adequate README | Incomplete |

---

## Suggested Timeline (Week 8)

| Day | Task |
|-----|------|
| 1–2 | Finalize option; update architecture diagram |
| 3–4 | Implement core infrastructure |
| 5 | Wire CI/CD and security checks |
| 6 | Cost + security writeups |
| 7 | Presentation rehearsal and submission |

---

## Presentation Outline

1. Problem and business context (2 min)
2. Architecture walkthrough (5 min)
3. Live or recorded Terraform / CI demo (5 min)
4. Security and cost highlights (3 min)
5. Lessons learned and next steps (2 min)
