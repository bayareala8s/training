# Enterprise Capstone Project

**Module 10** · Final assessment (30% of course grade)

---

## Choose Your Scenario

### Option 1 – Banking Regulatory Data Platform

Build a reporting platform for financial data.

**Requirements:**
- Ingest settlement and transaction data from multiple sources
- Transform data for regulatory reporting (e.g., daily settlement reports)
- Implement audit trails and data lineage
- Enforce strict access controls and encryption
- Generate compliance-ready datasets

**Sample datasets:** Transaction logs, settlement files, customer account summaries

---

### Option 2 – Healthcare Analytics Platform

Create secure patient analytics workflows.

**Requirements:**
- Ingest patient records and medical reporting data
- Apply PII protection and masking
- Build HIPAA-aware governance controls
- Create analytics datasets for operational reporting
- Implement comprehensive audit logging

**Sample datasets:** Patient demographics, appointment records, lab results (synthetic)

---

### Option 3 – E-Commerce Analytics Lakehouse

Build customer and sales analytics pipelines.

**Requirements:**
- Ingest sales, inventory, and customer behavior data
- Build star schema for sales analytics
- Implement real-time and batch ingestion patterns
- Create dashboards for business KPIs
- Optimize query costs for ad-hoc analytics

**Sample datasets:** Orders, products, customers, clickstream events

---

### Option 4 – Enterprise Data Platform

Develop a complete cloud-native data engineering platform.

**Requirements:**
- Full Raw → Cleaned → Curated data lake
- Multiple ingestion patterns (file, API, event-driven)
- Production ETL with schema evolution
- Data quality framework with quarantine
- Orchestration with Step Functions
- Security, governance, monitoring, and cost controls

---

## Required Deliverables

| Deliverable | Format |
|-------------|--------|
| Architecture diagrams | Draw.io, Lucidchart, or Mermaid |
| ETL workflows | Step Functions definitions + Glue jobs |
| Glue jobs | Python/PySpark scripts in `src/` |
| Data catalogs | Glue Data Catalog screenshots or exports |
| Monitoring dashboards | CloudWatch dashboard JSON or screenshots |
| Governance controls | IAM policies, encryption config, audit logs |
| Cost analysis | Cost Explorer report or spreadsheet |
| Final presentation | 15–20 minute slide deck |

---

## Project Structure

```text
capstone/
├── README.md                      # This file
├── rubric.md                      # Detailed grading rubric
├── presentation-guide.md          # 15–20 min presentation structure
├── templates/
│   └── project-structure/         # Full starter template (copy this)
│       ├── README.md
│       ├── docs/
│       │   ├── ARCHITECTURE.md
│       │   ├── GOVERNANCE.md
│       │   └── COST-ANALYSIS.md
│       ├── src/                   # ingestion, etl, validation
│       ├── infrastructure/
│       ├── architecture/diagrams/
│       └── presentation/slides/
└── my-project/                    # Your deployed capstone (you create)
```

**Start here:**

```bash
cp -r capstone/templates/project-structure capstone/my-project
```

See also [Module 10 capstone checklist](../modules/module-10-capstone/assignments/capstone-checklist.md).

---

## Evaluation Rubric

See **[capstone/rubric.md](./rubric.md)** for the full grading rubric with point scales, evaluator checklists, and self-assessment worksheet.

| Criterion | Weight |
|-----------|--------|
| Architecture & Design | 25% |
| Implementation Quality | 25% |
| Data Quality & Governance | 20% |
| Monitoring & Operations | 15% |
| Documentation & Presentation | 15% |

---

## Submission Checklist

- [ ] All code committed to GitHub repository
- [ ] README with setup and deployment instructions
- [ ] Architecture diagram included
- [ ] All AWS resources tagged with `Project=capstone` and `Student=<name>`
- [ ] Cost analysis completed
- [ ] Presentation submitted before final session

---

## Getting Started

1. Choose your capstone option
2. Copy the template: `cp -r capstone/templates/project-structure capstone/my-project`
3. Review [Module 10 README](../modules/module-10-capstone/README.md) and [Week 10 Lecture](../modules/module-10-capstone/lectures/week-10-lecture.md)
4. Follow the [capstone checklist](../modules/module-10-capstone/assignments/capstone-checklist.md)
5. Read [presentation-guide.md](./presentation-guide.md) before build week ends
6. Begin with architecture design before implementation
