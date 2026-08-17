# Cloud-Native Data Engineering on AWS

> **Design, Build, Automate, Secure, and Operate Enterprise Data Platforms on AWS**

**Offered by [BayAreaLa8s](https://bayareala8s.com)**

| | |
|---|---|
| **Duration** | 10 Weeks · 72 Hours |
| **Format** | Instructor-Led / Hybrid / Self-Paced |
| **Level** | Intermediate → Advanced |

---

## Course Description

Modern organizations generate massive amounts of structured and unstructured data from applications, APIs, IoT devices, vendors, financial systems, and customer interactions.

The challenge is not collecting data. The challenge is:

- Ingesting data reliably
- Transforming data efficiently
- Ensuring data quality
- Managing costs
- Enforcing governance
- Supporting analytics and AI

This course teaches students how to build **production-grade cloud-native data platforms** using AWS services. Unlike theory-heavy courses, students will build complete production-ready data platforms.

---

## Target Audience

- Data Engineers
- Data Analysts transitioning to Engineering
- Data Scientists
- Cloud Engineers
- DevOps Engineers
- Software Engineers
- Platform Engineers
- Students pursuing Data Engineering careers

---

## Prerequisites

Students should have:

- Basic SQL knowledge
- Basic Python programming
- AWS fundamentals
- Linux fundamentals
- Basic understanding of databases
- Familiarity with data concepts

---

## Learning Outcomes

By the end of this course students will be able to:

- Design cloud-native data architectures
- Build event-driven ingestion pipelines
- Implement scalable ETL workflows
- Create data lakes on AWS
- Build metadata-driven pipelines
- Perform data quality validation
- Secure enterprise datasets
- Monitor and troubleshoot pipelines
- Optimize costs and performance
- Support analytics and AI workloads

---

## Architecture Students Build

```text
Data Sources
(APIs, Files, Events)
        |
EventBridge / S3 Events
        |
Lambda Ingestion Layer
        |
S3 Data Lake
Raw → Cleaned → Curated
        |
AWS Glue ETL
        |
Glue Data Catalog
        |
Athena Analytics
        |
CloudWatch Monitoring
        |
Dashboards & Alerts
```

---

## Technologies Covered

### AWS Services

Amazon S3 · AWS Glue · AWS Lambda · Amazon EventBridge · AWS Step Functions · Amazon Athena · Amazon DynamoDB · Amazon CloudWatch · IAM · AWS Secrets Manager

### Data Technologies

SQL · Python · Pandas · PySpark (optional advanced track) · JSON · Parquet · CSV

### DevOps & Automation

Terraform · GitHub · GitHub Actions · Docker (optional)

---

## Repository Structure

```text
.
├── README.md                 # Course overview (this file)
├── docs/
│   ├── SYLLABUS.md           # Full 10-module syllabus
│   ├── ASSESSMENT.md         # Grading and deliverables
│   └── CAREER-OUTCOMES.md    # Portfolio and career guidance
├── modules/
│   ├── module-01-foundations/
│   ├── module-02-ingestion/
│   ├── module-03-glue-etl/
│   ├── module-04-data-quality/
│   ├── module-05-modeling-analytics/
│   ├── module-06-orchestration/
│   ├── module-07-security-governance/
│   ├── module-08-monitoring-ops/
│   ├── module-09-ai-ml-data/
│   └── module-10-capstone/
├── labs/                     # Hands-on lab exercises
├── capstone/                 # Capstone project templates
└── infrastructure/           # Terraform and IaC templates
```

---

## Assessment Structure

| Assessment | Weight |
|------------|--------|
| Weekly Labs | 30% |
| Assignments | 20% |
| Architecture Reviews | 10% |
| Data Platform Project | 10% |
| Capstone Project | 30% |

See [docs/ASSESSMENT.md](docs/ASSESSMENT.md) for details.

---

## Student Portfolio Outcomes

Students graduate with:

- Enterprise data lake architecture
- Production ETL pipelines
- Event-driven data workflows
- Data quality framework
- Governance implementation
- Monitoring dashboards
- AI-ready data platform
- Resume-ready GitHub repositories

---

## Resume Outcome Example

> Designed and implemented a cloud-native data platform on AWS using S3, Glue, Lambda, Athena, Step Functions, and CloudWatch to ingest, transform, validate, govern, and analyze enterprise-scale datasets with automated monitoring and cost controls.

---

## BayAreaLa8s Academy

This course complements the BayAreaLa8s flagship curriculum:

1. Enterprise File Transfer Automation on AWS
2. Terraform for Real Enterprises
3. AI Automation & Agents with AWS Bedrock
4. **Cloud-Native Data Engineering on AWS** ← you are here
5. Production-Grade Microservices on AWS

Together, these create a complete **Cloud, Data, AI, DevOps, and Platform Engineering Academy**.

---

## Course Content

This repository contains **complete professional course materials**:

| Content | Count |
|---------|-------|
| Modules | 10 weeks |
| Lectures | 10 (2 hours each) |
| Hands-on labs | 26 with code |
| Assignments | 9 + capstone |
| Terraform modules | 6 |
| Instructor guide | Included |

**Full navigation:** [docs/COURSE-INDEX.md](docs/COURSE-INDEX.md) · **Lab demo guide:** [docs/LAB-DEMO-GUIDE.md](docs/LAB-DEMO-GUIDE.md) · **Diagrams:** [docs/diagrams/](docs/diagrams/README.md)

---

## Deploy & Teardown Scripts

Use the scripts in [`scripts/`](scripts/) to deploy and destroy all lab AWS resources:

```bash
./scripts/lab-cycle.sh start       # Start labs
./scripts/lab-cycle.sh stop --yes    # Stop labs (zero ongoing cost)
./scripts/lab-cycle.sh status        # Check what's running
./scripts/test-all-labs.sh           # Full validation (~40 min, tears down)
```

**Step-by-step demo for all 26 labs:** [docs/LAB-DEMO-GUIDE.md](docs/LAB-DEMO-GUIDE.md)

See [scripts/README.md](scripts/README.md) for details.

---

## Getting Started

1. Read the [Student Handbook](docs/STUDENT-HANDBOOK.md)
2. Complete [Environment Setup](setup/SETUP.md)
3. Review the [full syllabus](docs/SYLLABUS.md)
4. Begin [Module 1 – Foundations](modules/module-01-foundations/)

---

## License

Course materials © BayAreaLa8s. All rights reserved.
