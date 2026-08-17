# Module 4 – Data Quality & Reliability

**Week 4** · ~7 hours

## Learning Objectives

- Define data quality dimensions and translate business rules into technical validation
- Build a reusable validation framework with declarative JSON rule definitions
- Integrate validation into Lambda and Glue ETL pipelines
- Design quarantine zones for bad-record isolation and replay workflows
- Apply reliability engineering patterns (SLIs, SLOs, error budgets) to data pipelines
- Generate quality reports and operational alerts for stakeholders

## Topics

- Data Quality Dimensions (completeness, validity, accuracy, timeliness)
- Declarative Validation Rules (`not_null`, `range`, `enum`, `regex`)
- Error Handling and Fail-Safe Routing
- Quarantine Zone Architecture and Replay
- Reliability Engineering (SLIs, SLOs, error budgets)
- Great Expectations Concepts and AWS Alternatives (Deequ, Glue Data Quality)

## Week Schedule

| Day | Activity | Duration | Materials |
|-----|----------|----------|-----------|
| **Mon** | Lecture: Data Quality & Reliability Engineering | 2h | [Week 4 Lecture](lectures/week-04-lecture.md) |
| **Tue** | Lab 4.1: Build validation framework | 2h | [Lab 4.1](labs/lab-4.1-quality-framework/README.md) |
| **Wed** | Lab 4.2: Lambda/Glue validation automation | 1.5h | [Lab 4.2](labs/lab-4.2-validation-automation/README.md) |
| **Thu** | Lab 4.3: Quarantine zone and replay workflow | 1.5h | [Lab 4.3](labs/lab-4.3-quarantine-zone/README.md) |
| **Fri** | Assignment 4: Data quality SLAs for RetailCo | 2h | [Assignment 4](assignments/assignment-04.md) |

## Hands-On Labs

| Lab | Description |
|-----|-------------|
| [Lab 4.1](labs/lab-4.1-quality-framework/README.md) | Python validation library with JSON rules; pass/quarantine routing |
| [Lab 4.2](labs/lab-4.2-validation-automation/README.md) | Integrate validators into Lambda and Glue; CloudWatch metrics and SNS |
| [Lab 4.3](labs/lab-4.3-quarantine-zone/README.md) | Quarantine isolation, steward review, replay to cleaned zone |

## Deliverables

- [ ] Working validation framework (`validators.py`, `quality_runner.py`)
- [ ] Quality report JSON with pass rate and violation breakdown
- [ ] Quarantine records uploaded to S3 with manifest
- [ ] CloudWatch metrics and pass-rate alarm (Lab 4.2)
- [ ] Assignment 4: SLA document with rules catalog for orders and inventory

## Key AWS Services

AWS Lambda · AWS Glue · Amazon S3 · Amazon CloudWatch · Amazon SNS · Amazon Athena

## Reading & Resources

- [Week 4 Lecture](lectures/week-04-lecture.md)
- [AWS Glue Data Quality](https://docs.aws.amazon.com/glue/latest/dg/glue-data-quality.html)
- [Great Expectations Documentation](https://docs.greatexpectations.io/)
- [Amazon Deequ (GitHub)](https://github.com/awslabs/deequ)
- [Google SRE — Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)

## Previous Module

← [Module 3 – Glue ETL](../module-03-glue-etl/README.md)

## Next Module

→ [Module 5 – Data Modeling & Analytics](../module-05-modeling-analytics/README.md)
