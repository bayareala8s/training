# Module 1 – Modern Data Engineering Foundations

**Week 1** · ~7 hours

---

## Week Schedule

| Day | Activity | Resource | Time |
|-----|----------|----------|------|
| Mon | Lecture: Data engineering foundations | [week-01-lecture.md](lectures/week-01-lecture.md) | 2 hrs |
| Tue | Lab 1.1: Build S3 Data Lake | [lab-1.1](labs/lab-1.1-build-s3-data-lake/README.md) | 1.5 hrs |
| Wed | Lab 1.2: Raw / Cleaned / Curated zones | [lab-1.2](labs/lab-1.2-data-lake-zones/README.md) | 1.5 hrs |
| Thu | Assignment 1: Architecture design | [assignment-01.md](assignments/assignment-01.md) | 1.5 hrs |
| Fri | Review & prepare for Module 2 | [Student Handbook](../../docs/STUDENT-HANDBOOK.md) | 0.5 hrs |

---

## Learning Objectives

- Distinguish data engineering from data science and analytics
- Compare data lakes, data warehouses, and lakehouse patterns
- Understand batch vs streaming processing trade-offs
- Design a cloud-native data platform architecture
- Deploy an S3 data lake with Terraform

---

## Lecture

📖 **[Week 1 Lecture – Modern Data Engineering Foundations](lectures/week-01-lecture.md)**

Topics: data engineering roles, lake vs warehouse, medallion architecture, AWS data ecosystem, enterprise design principles.

---

## Hands-On Labs

| Lab | Description | Folder |
|-----|-------------|--------|
| **Lab 1.1** | Build S3 Data Lake with Terraform | [labs/lab-1.1-build-s3-data-lake/](labs/lab-1.1-build-s3-data-lake/README.md) |
| **Lab 1.2** | Raw / Cleaned / Curated zones + sample data | [labs/lab-1.2-data-lake-zones/](labs/lab-1.2-data-lake-zones/README.md) |

### Infrastructure

Terraform module: [infrastructure/modules/s3-data-lake/](../../infrastructure/modules/s3-data-lake/main.tf)

```bash
cd infrastructure/environments/dev
terraform init && terraform apply
```

---

## Assignment

📝 **[Assignment 1 – Data Platform Architecture Design](assignments/assignment-01.md)**

Design a cloud-native data platform for RetailCo e-commerce (2–3 pages + diagram).

---

## Module Deliverables

- [ ] S3 data lake deployed via Terraform
- [ ] Raw zone populated with partitioned sample orders
- [ ] Metadata manifest uploaded
- [ ] Architecture diagram (Lab 1.2 + Assignment 1)
- [ ] Assignment 1 submitted

---

## Key AWS Services

Amazon S3 · IAM · Terraform · AWS CLI

---

## Prerequisites

Complete [Environment Setup](../../setup/SETUP.md) before starting.

---

## Next Module

→ [Module 2 – Data Ingestion Patterns](../module-02-ingestion/README.md)
