# Student Handbook

**Cloud-Native Data Engineering on AWS** · BayAreaLa8s

---

## Welcome

This handbook covers everything you need to succeed in the course: environment setup, weekly workflow, submission guidelines, and AWS cost management.

---

## Weekly Workflow

Each week follows this rhythm (~7 hours):

| Day | Activity | Time |
|-----|----------|------|
| 1 | Read lecture notes, watch instructor session | 2 hrs |
| 2–3 | Complete hands-on labs | 3 hrs |
| 4 | Finish assignment | 1.5 hrs |
| 5 | Review, quiz, prepare for next week | 0.5 hrs |

### Week-by-Week Navigation

| Week | Module | Folder |
|------|--------|--------|
| 1 | Modern Data Engineering Foundations | [module-01-foundations](../modules/module-01-foundations/) |
| 2 | Data Ingestion Patterns | [module-02-ingestion](../modules/module-02-ingestion/) |
| 3 | AWS Glue ETL Engineering | [module-03-glue-etl](../modules/module-03-glue-etl/) |
| 4 | Data Quality & Reliability | [module-04-data-quality](../modules/module-04-data-quality/) |
| 5 | Data Modeling & Analytics | [module-05-modeling-analytics](../modules/module-05-modeling-analytics/) |
| 6 | Orchestration & Workflow Automation | [module-06-orchestration](../modules/module-06-orchestration/) |
| 7 | Security, Governance & Compliance | [module-07-security-governance](../modules/module-07-security-governance/) |
| 8 | Monitoring, Cost Optimization & Operations | [module-08-monitoring-ops](../modules/module-08-monitoring-ops/) |
| 9 | Data Engineering for AI & ML | [module-09-ai-ml-data](../modules/module-09-ai-ml-data/) |
| 10 | Enterprise Capstone Project | [module-10-capstone](../modules/module-10-capstone/) |

---

## Environment Setup

Complete [setup/SETUP.md](../setup/SETUP.md) before Week 1.

Required tools:

- AWS account (free tier eligible for most labs)
- AWS CLI v2
- Python 3.10+
- Terraform 1.5+
- Git
- VS Code or preferred IDE

---

## AWS Cost Management

Labs are designed to minimize cost. Follow these rules:

1. **Tag all resources** with `Project=cnde-course` and `Student=your-name`
2. **Destroy resources** after each lab session: `terraform destroy`
3. **Set a budget alert** at $20/month in AWS Budgets
4. **Use `us-east-1`** unless instructed otherwise (lowest cost region)
5. **Stop Glue jobs** if a lab runs longer than expected

Estimated total course cost: **$15–$40** depending on usage.

---

## Submission Guidelines

### Labs

- Commit code to your GitHub repository
- Include a `LAB-REPORT.md` in each lab folder with:
  - What you built
  - Screenshots of key AWS console views
  - Any issues encountered and how you resolved them

### Assignments

- Submit as Markdown or PDF via your learning platform
- Include architecture diagrams where requested
- Cite AWS documentation for design decisions

### Capstone

- Public or private GitHub repository (share link with instructor)
- All deliverables listed in [capstone/README.md](../capstone/README.md)
- 15–20 minute presentation

---

## Getting Help

1. Check the lab troubleshooting section first
2. Search [AWS Documentation](https://docs.aws.amazon.com/)
3. Post in the course discussion forum
4. Office hours: see your cohort schedule

---

## Academic Integrity

- You may discuss concepts with classmates
- All submitted code and written work must be your own
- Using AI assistants for learning is encouraged; copying solutions without understanding is not
- Cite any external code or templates used

---

## Portfolio Building

By course end, your GitHub repository should demonstrate:

- Infrastructure as Code (Terraform)
- Serverless ingestion (Lambda, EventBridge)
- ETL pipelines (Glue, PySpark)
- Data quality frameworks
- Orchestration (Step Functions)
- Security and governance controls
- Monitoring dashboards

Use this resume bullet when complete:

> Designed and implemented a cloud-native data platform on AWS using S3, Glue, Lambda, Athena, Step Functions, and CloudWatch to ingest, transform, validate, govern, and analyze enterprise-scale datasets with automated monitoring and cost controls.
