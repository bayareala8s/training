# Module 5 – Data Modeling & Analytics

**Week 5** · ~7 hours

## Learning Objectives

- Apply dimensional modeling and star schema design for lakehouse analytics
- Implement partitioning strategies aligned with Athena query patterns
- Optimize Athena queries for performance and cost (pruning, projection, joins)
- Build analytics-ready curated datasets from Module 3 cleaned data
- Establish cost-efficient reporting patterns (summaries, views, workgroups)

## Topics

- Dimensional Modeling and Star Schemas
- Slowly Changing Dimensions (SCD)
- Hive-Style Partitioning on S3
- Athena Performance Tuning and Data Scanned Metrics
- Pre-Aggregation, Views, and Workgroup Governance

## Week Schedule

| Day | Activity | Duration | Materials |
|-----|----------|----------|-----------|
| **Mon** | Lecture: Data Modeling & Analytics on the Lake | 2h | [Week 5 Lecture](lectures/week-05-lecture.md) |
| **Tue** | Lab 5.1: Build star schema (dim_*, fact_orders) | 2h | [Lab 5.1](labs/lab-5.1-star-schema/README.md) |
| **Wed** | Lab 5.2: Athena query optimization (before/after) | 1.5h | [Lab 5.2](labs/lab-5.2-athena-optimization/README.md) |
| **Thu** | Lab 5.3: Cost-efficient query patterns | 1.5h | [Lab 5.3](labs/lab-5.3-cost-efficient-queries/README.md) |
| **Fri** | Assignment 5: E-commerce analytics model design | 2h | [Assignment 5](assignments/assignment-05.md) |

## Hands-On Labs

| Lab | Description |
|-----|-------------|
| [Lab 5.1](labs/lab-5.1-star-schema/README.md) | Athena DDL + CTAS for `dim_customer`, `dim_product`, `fact_orders` |
| [Lab 5.2](labs/lab-5.2-athena-optimization/README.md) | Before/after scan metrics; EXPLAIN and partition checks |
| [Lab 5.3](labs/lab-5.3-cost-efficient-queries/README.md) | Summary tables, analyst views, workgroup configuration |

## Deliverables

- [ ] Star schema tables in Glue catalog under `curated/retail/`
- [ ] Lab 5.1 validation queries pass (0 orphan fact rows)
- [ ] Lab 5.2 scan reduction report with before/after metrics
- [ ] `daily_revenue_summary` table and analyst views (Lab 5.3)
- [ ] Assignment 5: Analytics model design document for RetailCo

## Key AWS Services

Amazon Athena · AWS Glue Data Catalog · Amazon S3 · AWS Glue (CTAS source data)

## Reading & Resources

- [Week 5 Lecture](lectures/week-05-lecture.md)
- [Athena Performance Tuning](https://docs.aws.amazon.com/athena/latest/ug/performance-tuning.html)
- [Partitioning Data in Athena](https://docs.aws.amazon.com/athena/latest/ug/partitions.html)

## Previous Module

← [Module 4 – Data Quality](../module-04-data-quality/README.md)

## Next Module

→ [Module 6 – Orchestration & Workflow Automation](../module-06-orchestration/README.md)
