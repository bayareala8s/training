# Week 8 – Capstone Project

Choose **one** option for your graded submission (30% of course grade).  
**Reference implementations** for all four tracks are included below so instructors can demo and students can study patterns.

---

## Reference implementations (ready)

| Option | Folder | What it includes |
|--------|--------|------------------|
| **1 – Enterprise Landing Zone** | [option-01-landing-zone/](option-01-landing-zone/) | Shared + workload-dev stacks, account model, CI, security/cost docs |
| **2 – Shared Services Platform** | [option-02-shared-services/](option-02-shared-services/) | Hub + spoke-dev, remote-state interface, TGW pattern docs |
| **3 – Multi-Region DR** | [option-03-multi-region-dr/](option-03-multi-region-dr/) | Primary `us-west-2` + secondary `us-east-1`, failover runbook |
| **4 – Internal Terraform Platform** | [option-04-terraform-platform/](option-04-terraform-platform/) | `network-baseline` + `app-host` modules, golden path, CI template |

Lab guide: [labs/week-08/LAB-capstone.md](../labs/week-08/LAB-capstone.md)

### Apply any option (pattern)

```bash
cd capstone/option-0N-.../terraform/environments/<env>
cp backend.hcl.example backend.hcl
cp terraform.tfvars.example terraform.tfvars
# edit owner / bucket as needed
terraform init -backend-config=backend.hcl
terraform plan -var-file=terraform.tfvars
terraform apply -var-file=terraform.tfvars
```

Tag resources with `Course=terraform-enterprise` (already set). Use `make lab-pause` from course root after demos.

---

## Option 1 – Enterprise Landing Zone

Deploy secure multi-account AWS foundation infrastructure.

**Must include:**

- OU/account model (design doc)
- Shared networking or security baseline (VPC, flow logs, or equivalent)
- Remote state per account or environment
- CI/CD with plan on PR

**Reference:** [option-01-landing-zone/README.md](option-01-landing-zone/README.md)

---

## Option 2 – Shared Services Platform

Build centralized networking and monitoring platform.

**Must include:**

- Hub VPC or transit-style design (simplified acceptable for cohort)
- Centralized logging or monitoring (CloudWatch, flow logs)
- Consumable outputs for spoke/workload accounts (subnets, TGW attachment pattern, or documented interface)

**Reference:** [option-02-shared-services/README.md](option-02-shared-services/README.md)

---

## Option 3 – Multi-Region DR Infrastructure

Create disaster recovery–enabled infrastructure deployment.

**Must include:**

- Primary and secondary region resources (or active-passive design)
- State and config strategy for failover
- Runbook for failover / failback (tabletop acceptable)

**Reference:** [option-03-multi-region-dr/README.md](option-03-multi-region-dr/README.md)

---

## Option 4 – Internal Terraform Platform

Build reusable Terraform platform for internal teams.

**Must include:**

- Module library (≥2 modules) with versioning
- Golden path documentation for service teams
- CI template or workflow reusable by consumers

**Reference:** [option-04-terraform-platform/README.md](option-04-terraform-platform/README.md)

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

Students may **fork a reference implementation and extend it**, or build from scratch. Graded work must include original analysis (security, cost, presentation)—not an unmodified copy.

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
