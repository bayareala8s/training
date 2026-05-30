# Module 6 – Orchestration & Workflow Automation

**Week 6** · ~7 hours

## Learning Objectives

- Design multi-stage ETL workflows with AWS Step Functions Standard workflows
- Implement pipeline scheduling with EventBridge and dependency management
- Configure retry, Catch, and Choice states for error branching
- Build failure recovery with SNS notifications and operational runbooks
- Deploy state machines via Terraform (`infrastructure/modules/step-functions`)

## Topics

- AWS Step Functions and Amazon States Language (ASL)
- Glue `startJobRun.sync` and Lambda integrations
- Retry, Backoff, and Jitter
- Choice States and Quality SLO Gates
- EventBridge Scheduling and Idempotency
- SNS Alerting and Runbooks

## Week Schedule

| Day | Activity | Duration | Materials |
|-----|----------|----------|-----------|
| **Mon** | Lecture: Orchestration & Workflow Automation | 2h | [Week 6 Lecture](lectures/week-06-lecture.md) |
| **Tue** | Lab 6.1: Multi-stage ETL Step Functions workflow | 2h | [Lab 6.1](labs/lab-6.1-step-functions-etl/README.md) |
| **Wed** | Lab 6.2: Retry automation and error branching | 1.5h | [Lab 6.2](labs/lab-6.2-retry-error-branching/README.md) |
| **Thu** | Lab 6.3: Failure handling with SNS notifications | 1.5h | [Lab 6.3](labs/lab-6.3-sns-failure-handling/README.md) |
| **Fri** | Assignment 6: Multi-source orchestration design | 2h | [Assignment 6](assignments/assignment-06.md) |

## Hands-On Labs

| Lab | Description |
|-----|-------------|
| [Lab 6.1](labs/lab-6.1-step-functions-etl/README.md) | Lambda → Glue → quality gate state machine; ASL in `src/` |
| [Lab 6.2](labs/lab-6.2-retry-error-branching/README.md) | Retry blocks, warning path, non-retriable error classification |
| [Lab 6.3](labs/lab-6.3-sns-failure-handling/README.md) | SNS publish on failure; operational runbook |

## Infrastructure

| Resource | Path |
|----------|------|
| Step Functions Terraform module | [`infrastructure/modules/step-functions/main.tf`](../../infrastructure/modules/step-functions/main.tf) |
| Default ASL template | [`infrastructure/modules/step-functions/templates/`](../../infrastructure/modules/step-functions/templates/) |

## Deliverables

- [ ] State machine deployed (Terraform or CLI)
- [ ] Successful end-to-end execution for `processing_date`
- [ ] Failed execution with retry events documented (Lab 6.2)
- [ ] SNS failure alert received (Lab 6.3)
- [ ] `RUNBOOK.md` for on-call response
- [ ] Assignment 6: Multi-source orchestration design document

## Key AWS Services

AWS Step Functions · AWS Glue · AWS Lambda · Amazon EventBridge · Amazon SNS · Amazon CloudWatch · AWS IAM

## Reading & Resources

- [Week 6 Lecture](lectures/week-06-lecture.md)
- [Step Functions Developer Guide](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html)
- [Step Functions Error Handling](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html)

## Previous Module

← [Module 5 – Data Modeling & Analytics](../module-05-modeling-analytics/README.md)

## Next Module

→ [Module 7 – Security, Governance & Compliance](../module-07-security-governance/README.md)
