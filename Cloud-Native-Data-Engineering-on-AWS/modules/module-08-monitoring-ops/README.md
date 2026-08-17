# Module 8 – Monitoring, Cost Optimization & Operations

**Week 8** · ~7 hours

## Learning Objectives

- Build CloudWatch dashboards for pipeline observability
- Configure alerts for pipeline failures and SLA breaches
- Implement cost allocation and reporting
- Apply operational excellence practices to data platforms
- Write incident runbooks for production data operations

## Topics

- CloudWatch Monitoring
- Data Pipeline Observability
- Cost Allocation
- Alerting & Anomaly Detection
- Operational Excellence
- Incident Response

## Lecture

- [Week 8 Lecture – Monitoring, Cost Optimization & Operations](lectures/week-08-lecture.md)

## Hands-On Labs

| Lab | Description | Time |
|-----|-------------|------|
| [Lab 8.1](labs/lab-8.1-cloudwatch-dashboards/README.md) | CloudWatch dashboards for ETL pipelines (JSON in `src/`) | 90 min |
| [Lab 8.2](labs/lab-8.2-sns-alerts/README.md) | SNS alerts and anomaly detection setup | 90 min |
| [Lab 8.3](labs/lab-8.3-cost-reporting/README.md) | Cost reporting with tags and Cost Explorer guide | 75 min |

## Assignment

- [Assignment 8 – Operations Runbook for Data Platform Incidents](assignments/assignment-08.md)

## Infrastructure

Terraform monitoring module: [`infrastructure/modules/monitoring/main.tf`](../../infrastructure/modules/monitoring/main.tf)

Deploys CloudWatch dashboards, alarms, and SNS topics for the course data platform.

## Deliverables

- [ ] CloudWatch ETL operations dashboard
- [ ] SNS alert routing (critical + warning)
- [ ] Cost Explorer report with tag filters
- [ ] Operations incident runbook (Assignment 8)

## Key AWS Services

Amazon CloudWatch · AWS Cost Explorer · Amazon SNS · AWS Budgets · AWS Glue · AWS Lambda

## Reading & Resources

- [CloudWatch Best Practices – Recommended Alarms](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Best_Practice_Recommended_Alarms_AWS_Services.html)
- [AWS Cost Allocation Tags](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html)
- [AWS Glue Monitoring](https://docs.aws.amazon.com/glue/latest/dg/monitor-glue.html)

## Previous Module

← [Module 7 – Security & Governance](../module-07-security-governance/README.md)

## Next Module

→ [Module 9 – Data Engineering for AI & ML](../module-09-ai-ml-data/README.md)
