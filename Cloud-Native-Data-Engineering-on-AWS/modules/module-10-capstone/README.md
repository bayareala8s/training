# Module 10 – Enterprise Capstone Project

**Week 10** · ~8 hours

## Overview

The capstone integrates all course modules into a production-grade enterprise data platform. Students select one of four industry scenarios and deliver a complete, documented solution.

## Learning Objectives

- Integrate ingestion, ETL, quality, governance, monitoring, and cost controls into one platform
- Deploy and document a capstone project using Infrastructure as Code
- Present a technical solution to technical and non-technical stakeholders
- Produce portfolio-ready architecture and operations documentation

## Lecture

- [Week 10 Lecture – Capstone Kickoff, Project Management & Presentation](lectures/week-10-lecture.md)

## Capstone Options

| Option | Industry | Focus |
|--------|----------|-------|
| **Option 1** | Banking | Regulatory reporting data platform |
| **Option 2** | Healthcare | Secure patient analytics workflows |
| **Option 3** | E-Commerce | Customer and sales analytics lakehouse |
| **Option 4** | Enterprise | Complete cloud-native data platform |

See [capstone/README.md](../../capstone/README.md) for detailed requirements.

## Project Template

Copy and customize the full project scaffold:

```bash
cp -r capstone/templates/project-structure capstone/my-project
```

Template includes:

| File | Purpose |
|------|---------|
| [README.md](../../capstone/templates/project-structure/README.md) | Setup, deploy, verify, cleanup |
| [ARCHITECTURE.md](../../capstone/templates/project-structure/docs/ARCHITECTURE.md) | Design decisions and diagrams |
| [GOVERNANCE.md](../../capstone/templates/project-structure/docs/GOVERNANCE.md) | Security and compliance |
| [COST-ANALYSIS.md](../../capstone/templates/project-structure/docs/COST-ANALYSIS.md) | Cost breakdown and optimizations |

## Capstone Resources

| Resource | Description |
|----------|-------------|
| [Capstone README](../../capstone/README.md) | Scenarios and deliverables |
| [Grading Rubric](../../capstone/rubric.md) | Detailed evaluation criteria |
| [Presentation Guide](../../capstone/presentation-guide.md) | 15–20 min structure and demo script |
| [Milestone Checklist](assignments/capstone-checklist.md) | Day-by-day capstone progress tracker |

## Required Deliverables

- [ ] Architecture diagrams (context + component)
- [ ] ETL workflows (Glue jobs + optional Step Functions)
- [ ] Data catalogs (Glue Data Catalog)
- [ ] Monitoring dashboards (CloudWatch)
- [ ] Governance controls (IAM, encryption, GOVERNANCE.md)
- [ ] Cost analysis (COST-ANALYSIS.md)
- [ ] Final presentation (15–20 minutes)

## Evaluation Criteria

| Criterion | Weight | Details |
|-----------|--------|---------|
| Architecture & Design | 25% | [rubric.md](../../capstone/rubric.md) |
| Implementation Quality | 25% | |
| Data Quality & Governance | 20% | |
| Monitoring & Operations | 15% | |
| Documentation & Presentation | 15% | |

## Hands-On Workflow

| Day | Focus |
|-----|-------|
| 1 | Architecture design |
| 2 | Infrastructure + S3 zones |
| 3 | Ingestion + sample data |
| 4 | Glue ETL pipeline |
| 5 | Data quality + quarantine |
| 6 | Security + monitoring |
| 7 | Documentation + cost analysis |
| 8 | Presentation rehearsal |

Full checklist: [capstone-checklist.md](assignments/capstone-checklist.md)

## Key AWS Services

Amazon S3 · AWS Glue · AWS Lambda · Amazon Athena · AWS Step Functions · IAM · KMS · Amazon CloudWatch · Amazon SNS · AWS Cost Explorer

## Previous Module

← [Module 9 – AI & ML Data Engineering](../module-09-ai-ml-data/README.md)

## Course Complete

Congratulations on completing **Cloud-Native Data Engineering on AWS**!

Review your [portfolio outcomes](../../docs/CAREER-OUTCOMES.md) and update your resume.
