# Module 2 – Data Ingestion Patterns

**Week 2** · ~7 hours

## Learning Objectives

- Implement file-based and API-based ingestion patterns
- Build event-driven pipelines with Lambda and EventBridge
- Design incremental and idempotent load strategies
- Handle S3 event notifications for automated processing
- Apply least-privilege IAM and operational monitoring to ingestion workloads

## Topics

- File-Based Ingestion (landing, raw partitioning, validation)
- API Ingestion (scheduled pull, webhooks, pagination)
- Event-Driven Pipelines (Lambda, EventBridge, decoupling)
- Incremental Loads (watermarks, late-arriving data)
- Idempotent Processing (deterministic keys, at-least-once semantics)
- S3 Event Notifications (promotion, quarantine)

## Week 2 Schedule

| Day | Activity | Time | Resource |
|-----|----------|------|----------|
| Mon | Lecture: ingestion patterns | 2h | [week-02-lecture.md](lectures/week-02-lecture.md) |
| Tue | Lab 2.1: Lambda → S3 raw | 1.5h | [lab-2.1-lambda-ingestion](labs/lab-2.1-lambda-ingestion/README.md) |
| Wed | Lab 2.2: EventBridge schedule | 1.5h | [lab-2.2-eventbridge-automation](labs/lab-2.2-eventbridge-automation/README.md) |
| Thu | Lab 2.3: S3 event processing | 1.5h | [lab-2.3-s3-event-processing](labs/lab-2.3-s3-event-processing/README.md) |
| Fri | Assignment 2 + review | 0.5h | [assignment-02.md](assignments/assignment-02.md) |

**Total:** ~7 hours

## Hands-On Labs

| Lab | Description | Source |
|-----|-------------|--------|
| [Lab 2.1](labs/lab-2.1-lambda-ingestion/README.md) | Lambda ingestion pipeline — JSON records to S3 raw zone | [handler.py](labs/lab-2.1-lambda-ingestion/src/handler.py) |
| [Lab 2.2](labs/lab-2.2-eventbridge-automation/README.md) | EventBridge scheduled API fetch with watermarks | [scheduled_ingestion.py](labs/lab-2.2-eventbridge-automation/src/scheduled_ingestion.py) |
| [Lab 2.3](labs/lab-2.3-s3-event-processing/README.md) | S3 `ObjectCreated` triggers — promote or quarantine files | [s3_event_handler.py](labs/lab-2.3-s3-event-processing/src/s3_event_handler.py) |

## Infrastructure (Terraform)

Deploy all three Lambda functions, IAM, EventBridge rule, and S3 notifications:

```hcl
module "lambda_ingestion" {
  source           = "../../modules/lambda-ingestion"
  project          = var.project
  environment      = var.environment
  student          = var.student
  data_lake_bucket = module.data_lake.bucket_name
}
```

Module path: [infrastructure/modules/lambda-ingestion](../../infrastructure/modules/lambda-ingestion/main.tf)

**Prerequisite:** Module 1 `s3-data-lake` deployed in `infrastructure/environments/dev`.

## Deliverables

- [ ] Lab 2.1 report — idempotent Lambda writes verified in S3
- [ ] Lab 2.2 report — scheduled snapshot + watermark JSON
- [ ] Lab 2.3 report — S3 event promotion and quarantine demonstrated
- [ ] Assignment 2 — banking event-driven ingestion design (3–4 pages + diagram)
- [ ] Optional: Terraform `lambda-ingestion` module applied in dev environment

## Key AWS Services

AWS Lambda · Amazon EventBridge · Amazon S3 · IAM · Amazon CloudWatch · AWS Secrets Manager (production APIs)

## Reading & Resources

- [Week 2 Lecture](lectures/week-02-lecture.md)
- [AWS Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [Amazon EventBridge Scheduler](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-create-rule-schedule.html)
- [S3 Event Notifications](https://docs.aws.amazon.com/AmazonS3/latest/userguide/EventNotifications.html)

## Previous Module

← [Module 1 – Foundations](../module-01-foundations/README.md)

## Next Module

→ [Module 3 – AWS Glue ETL Engineering](../module-03-glue-etl/README.md)
