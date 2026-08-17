# Module 3 – AWS Glue ETL Engineering

**Week 3** · ~7 hours

## Learning Objectives

- Configure Glue Crawlers for automatic schema discovery
- Develop Glue ETL jobs with PySpark
- Manage datasets in the Glue Data Catalog
- Handle schema evolution in production pipelines
- Optimize ETL job performance and cost

## Topics

- Glue Crawlers
- Glue Jobs
- Data Catalog
- Schema Evolution
- ETL Optimization
- PySpark on Glue (DynamicFrame vs DataFrame, partitioning, Parquet)

---

## Week 3 Schedule

| Day | Activity | Time | Location |
|-----|----------|------|----------|
| **Mon** | Lecture: Glue architecture, catalog, crawlers | 2h | [Week 3 Lecture](lectures/week-03-lecture.md) |
| **Tue** | Lab 3.1: Raw → Cleaned ETL pipeline | 2h | [Lab 3.1](labs/lab-3.1-etl-raw-to-cleaned/README.md) |
| **Wed** | Lab 3.2: Crawlers & Data Catalog + Athena | 1.5h | [Lab 3.2](labs/lab-3.2-glue-crawlers/README.md) |
| **Thu** | Lab 3.3: Partitioning & Parquet optimization | 1.5h | [Lab 3.3](labs/lab-3.3-etl-optimization/README.md) |
| **Fri** | Assignment 3: Healthcare ETL design | — | [Assignment 3](assignments/assignment-03.md) |

**Recommended flow:** Lecture → Lab 3.1 → Lab 3.2 → Lab 3.3 → Assignment

---

## Hands-On Labs

| Lab | Description | Key Skills |
|-----|-------------|------------|
| [Lab 3.1](labs/lab-3.1-etl-raw-to-cleaned/README.md) | Build ETL pipeline: Raw CSV → Cleaned Parquet | Glue jobs, PySpark, Terraform |
| [Lab 3.2](labs/lab-3.2-glue-crawlers/README.md) | Catalog datasets with Glue Crawlers | Schema inference, Athena queries |
| [Lab 3.3](labs/lab-3.3-etl-optimization/README.md) | Optimize with partitioning and file sizing | DPU tuning, coalesce, scan reduction |

---

## Infrastructure

Deploy the Glue module via Terraform (see Lab 3.1):

```bash
cd infrastructure/environments/dev
terraform init && terraform apply
```

Terraform module: [`infrastructure/modules/glue-etl`](../../infrastructure/modules/glue-etl/main.tf)

Resources created:

- IAM role (Glue service + S3 scoped policies)
- Glue Data Catalog database
- Glue ETL job (`raw-to-cleaned`)
- Glue crawler (cleaned zone)
- S3 script placeholder at `glue/scripts/glue_etl_job.py`

---

## Deliverables

- [ ] Glue ETL job running successfully (Lab 3.1)
- [ ] Cleaned Parquet data with Hive partitions
- [ ] Data catalog tables queryable in Athena (Lab 3.2)
- [ ] Optimization playbook with baseline vs improved metrics (Lab 3.3)
- [ ] Assignment 3: Healthcare ETL architecture document

---

## Key AWS Services

AWS Glue · AWS Glue Data Catalog · Amazon S3 · IAM · Amazon Athena · AWS CloudWatch

---

## Reading & Resources

- [Week 3 Lecture](lectures/week-03-lecture.md)
- [AWS Glue Developer Guide](https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html)
- [AWS Glue Best Practices](https://docs.aws.amazon.com/glue/latest/dg/best-practices.html)
- [Optimizing Spark on Glue](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-performance.html)

---

## Previous Module

← [Module 2 – Data Ingestion](../module-02-ingestion/README.md)

## Next Module

→ [Module 4 – Data Quality & Reliability](../module-04-data-quality/README.md)
