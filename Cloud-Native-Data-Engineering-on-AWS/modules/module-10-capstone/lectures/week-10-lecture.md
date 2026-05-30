# Week 10 Lecture: Enterprise Capstone Kickoff

**Duration:** 2 hours · **Module 10**

---

## Learning Objectives

By the end of this lecture you will:

1. Select and scope a capstone scenario aligned with your career goals
2. Plan a 10-day capstone using week-by-week milestones
3. Apply project management practices for solo data platform builds
4. Structure professional documentation (architecture, governance, cost)
5. Deliver a compelling 15–20 minute technical presentation

---

## 1. Capstone Overview

The capstone is your **portfolio centerpiece**—a production-grade data platform design and implementation that integrates every module in this course.

### What You Are Building

Not a toy demo. A **documented, deployable, governable** data platform that could be explained to a hiring manager or engineering lead in 20 minutes.

### Integration Map

| Module | Capstone Integration |
|--------|---------------------|
| 1 – Foundations | S3 data lake zones, medallion architecture |
| 2 – Ingestion | Lambda, EventBridge, or S3 event patterns |
| 3 – Glue ETL | Raw → Cleaned → Curated pipelines |
| 4 – Data Quality | Validation rules, quarantine, quality reports |
| 5 – Modeling | Curated star schema or analytical datasets |
| 6 – Orchestration | Step Functions workflows |
| 7 – Security | IAM, encryption, PII handling, audit logs |
| 8 – Monitoring | CloudWatch dashboards, SNS alerts, cost tags |
| 9 – AI/ML Data | Feature pipeline or ML dataset zone (where applicable) |

---

## 2. Choose Your Scenario

See [capstone/README.md](../../capstone/README.md) for full requirements.

| Option | Industry | Best For |
|--------|----------|----------|
| **Option 1** | Banking | Compliance, audit trails, strict governance |
| **Option 2** | Healthcare | PII/PHI protection, HIPAA-aware design |
| **Option 3** | E-Commerce | High-volume analytics, star schemas, recommendations |
| **Option 4** | Enterprise | Breadth—full platform showcase |

### Scoping Decision Framework

Ask yourself:

1. **Career alignment** — Which scenario matches roles you're targeting?
2. **Evidence strength** — Can you demo ingestion + ETL + quality + monitoring?
3. **Time realism** — Can you deliver working code in 8 hours of focused build time?
4. **Differentiation** — What one feature makes your project memorable? (e.g., anomaly alerts, feature store, RAG pipeline)

**Recommendation:** Depth over breadth. A fully working e-commerce lakehouse with quality gates beats a shallow "everything" platform.

---

## 3. Project Management for Capstone

### Timeline (Week 10)

| Day | Focus | Output |
|-----|-------|--------|
| Mon | Scenario selection, architecture design | ARCHITECTURE.md draft, diagram v1 |
| Tue | Infrastructure + S3 zones | Terraform applied, zones verified |
| Wed | Ingestion + ETL | Glue jobs, at least one end-to-end path |
| Thu | Quality + orchestration | Validation rules, Step Functions (optional) |
| Fri | Security + monitoring | IAM, dashboards, SNS |
| Sat | Documentation + cost analysis | GOVERNANCE.md, COST-ANALYSIS.md |
| Sun | Presentation prep | Slides, demo script, rehearsal |

Detailed checklist: [assignments/capstone-checklist.md](../assignments/capstone-checklist.md)

### Work Breakdown Structure

```text
Capstone Project
├── Architecture & Design (25% of grade)
│   ├── Context diagram
│   ├── Component diagram
│   └── Data flow diagram
├── Implementation (25%)
│   ├── Infrastructure (Terraform)
│   ├── Ingestion code
│   ├── ETL scripts
│   └── Quality framework
├── Quality & Governance (20%)
│   ├── Validation rules
│   ├── IAM policies
│   └── GOVERNANCE.md
├── Operations (15%)
│   ├── CloudWatch dashboard
│   ├── Alarms
│   └── Runbook excerpt
└── Documentation & Presentation (15%)
    ├── README setup guide
    ├── COST-ANALYSIS.md
    └── 15–20 min presentation
```

### Risk Management

| Risk | Mitigation |
|------|------------|
| AWS cost overrun | Set $50 budget alert; destroy resources after demo |
| Glue job failures | Test early; keep sample data small |
| Scope creep | Freeze architecture by Day 2 |
| Demo failure | Record backup video; have screenshots |
| Time shortage | Prioritize: lake + 1 ETL + quality + dashboard |

---

## 4. Documentation Standards

Use templates in [capstone/templates/project-structure/](../../capstone/templates/project-structure/).

### Required Documents

| Document | Purpose | Audience |
|----------|---------|----------|
| **README.md** | Setup, deploy, verify | Evaluator running your code |
| **ARCHITECTURE.md** | Design decisions, trade-offs | Engineering lead |
| **GOVERNANCE.md** | Security, compliance, access | Security reviewer |
| **COST-ANALYSIS.md** | Spend breakdown, optimizations | FinOps / manager |

### README Must Include

1. Project title and scenario option
2. Prerequisites (AWS account, Terraform, Python)
3. Step-by-step deployment commands
4. How to verify success (CLI commands, expected outputs)
5. Cleanup instructions (`terraform destroy`)
6. Your name and contact (optional)

### Architecture Document Must Include

1. Problem statement and requirements
2. Architecture diagrams (minimum 2)
3. AWS service selection with justification
4. Data zone design with S3 path examples
5. Non-functional requirements (scale, cost, security, reliability)

---

## 5. Implementation Best Practices

### Repository Structure

Copy the template:

```bash
cp -r capstone/templates/project-structure capstone/my-project
cd capstone/my-project
# Rename and customize
```

Expected layout:

```text
my-project/
├── README.md
├── docs/
│   ├── ARCHITECTURE.md
│   ├── GOVERNANCE.md
│   └── COST-ANALYSIS.md
├── infrastructure/
│   └── terraform/
├── src/
│   ├── ingestion/
│   ├── etl/
│   └── validation/
├── architecture/
│   └── diagrams/
└── presentation/
    └── slides/
```

### Tagging Requirement

All AWS resources must include:

```text
Project=capstone
Student=<your-name>
Environment=dev
```

### Git Hygiene

- Meaningful commit messages
- No secrets in repository (use `.gitignore` for tfvars)
- Tag release: `git tag capstone-v1.0`

---

## 6. Presentation Guide

See [capstone/presentation-guide.md](../../capstone/presentation-guide.md) for full details.

### 15–20 Minute Structure

| Section | Time | Content |
|---------|------|---------|
| Hook & problem | 2 min | Business context, why this platform matters |
| Architecture | 5 min | Diagram walkthrough, key decisions |
| Live demo | 5 min | Deployed pipeline, dashboard, quality report |
| Governance & ops | 3 min | Security, monitoring, cost |
| Lessons & Q&A | 3–5 min | What you'd do differently; open questions |

### Demo Script Essentials

1. Show S3 zones with data
2. Trigger or show recent Glue job success
3. Query curated data in Athena (one SQL statement)
4. Show CloudWatch dashboard with metrics
5. Show quality report or quarantine path

**Always have screenshots** if live demo fails.

### Presentation Anti-Patterns

- Reading slides verbatim
- Diving into code line-by-line
- Skipping the business problem
- No mention of cost or governance
- Running over time (practice with timer)

---

## 7. Evaluation and Rubric

See [capstone/rubric.md](../../capstone/rubric.md) for detailed grading criteria.

### High-Level Weights

| Criterion | Weight |
|-----------|--------|
| Architecture & Design | 25% |
| Implementation Quality | 25% |
| Data Quality & Governance | 20% |
| Monitoring & Operations | 15% |
| Documentation & Presentation | 15% |

### What Distinguishes Excellent Projects

- **Working end-to-end path** with real sample data flowing Raw → Curated
- **Quality gate** that quarantines bad records with a report
- **Monitoring** with at least one meaningful alarm
- **Professional docs** an evaluator can follow without asking questions
- **Clear presentation** connecting technical choices to business value

---

## 8. Career Portfolio Tips

After capstone:

1. Update resume with bullet points (see [CAREER-OUTCOMES.md](../../docs/CAREER-OUTCOMES.md))
2. Add GitHub repository to LinkedIn featured section
3. Prepare 2-minute "elevator pitch" version of presentation
4. Export architecture diagram for portfolio site
5. Write a short blog post: "How I built X on AWS"

Example resume bullet:

> Designed and deployed a cloud-native data lake on AWS (S3, Glue, Athena) processing daily retail orders with automated quality validation, reducing bad-record propagation to analytics by implementing quarantine routing and CloudWatch SLO alerts.

---

## 9. Discussion Questions

1. How do you decide when the capstone is "done" vs "perfect"?
2. What is the minimum viable capstone that still scores well?
3. How would you explain your architecture to a non-technical executive in 60 seconds?
4. Which module was hardest to integrate, and why?
5. What would you automate next if you had two more weeks?

---

## 10. This Week's Deliverables

| Deliverable | Reference |
|-------------|-----------|
| Complete capstone project | [capstone/README.md](../../capstone/README.md) |
| Week-by-week checklist | [capstone-checklist.md](../assignments/capstone-checklist.md) |
| Project templates | [capstone/templates/project-structure/](../../capstone/templates/project-structure/) |
| Presentation | [presentation-guide.md](../../capstone/presentation-guide.md) |

---

## Further Reading

- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)
- [The Pyramid Principle (communication)](https://www.consulting-methodology.com/pyramid-principle/)
- Course [Assessment Structure](../../docs/ASSESSMENT.md)

---

**Next:** Copy [project template](../../capstone/templates/project-structure/README.md) and begin architecture design.
