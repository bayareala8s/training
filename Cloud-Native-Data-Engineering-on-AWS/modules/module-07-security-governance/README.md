# Module 7 – Security, Governance & Compliance

**Week 7** · ~7 hours

## Learning Objectives

- Design IAM policies and roles for least-privilege data zone access
- Implement SSE-KMS encryption and bucket policies for secure transport
- Apply PII/PHI classification, masking, and safe alerting practices
- Configure audit logging with CloudTrail, S3 access logs, and Athena history
- Establish governance models and complete security audit reports

## Topics

- IAM for Data Platforms and Zone-Based RBAC
- AWS KMS and S3 Bucket Policies
- PII/PHI Protection and Safe Pipeline Logging
- CloudTrail and Audit Evidence
- Lake Formation and Governance Operating Models
- HIPAA Technical Safeguards Mapping

## Week Schedule

| Day | Activity | Duration | Materials |
|-----|----------|----------|-----------|
| **Mon** | Lecture: Security, Governance & Compliance | 2h | [Week 7 Lecture](lectures/week-07-lecture.md) |
| **Tue** | Lab 7.1: KMS encryption and bucket policies | 2h | [Lab 7.1](labs/lab-7.1-kms-bucket-policies/README.md) |
| **Wed** | Lab 7.2: IAM role-based access for data zones | 1.5h | [Lab 7.2](labs/lab-7.2-iam-rbac-data-zones/README.md) |
| **Thu** | Lab 7.3: Governance validation and audit report | 1.5h | [Lab 7.3](labs/lab-7.3-governance-audit/README.md) |
| **Fri** | Assignment 7: HIPAA governance framework | 2h | [Assignment 7](assignments/assignment-07.md) |

## Hands-On Labs

| Lab | Description |
|-----|-------------|
| [Lab 7.1](labs/lab-7.1-kms-bucket-policies/README.md) | CMK, default SSE-KMS, secure bucket policy JSON |
| [Lab 7.2](labs/lab-7.2-iam-rbac-data-zones/README.md) | Engineer, analyst, steward IAM policies with Deny rules |
| [Lab 7.3](labs/lab-7.3-governance-audit/README.md) | Audit evidence script + report template |

## Deliverables

- [ ] KMS-encrypted data lake bucket (Lab 7.1)
- [ ] Three zone-scoped IAM roles tested with assume-role (Lab 7.2)
- [ ] Completed audit report from template (Lab 7.3)
- [ ] Assignment 7: HIPAA governance framework document

## Key AWS Services

IAM · AWS KMS · Amazon S3 · AWS CloudTrail · AWS Lake Formation · AWS Glue · Amazon Athena · Amazon SNS

## Reading & Resources

- [Week 7 Lecture](lectures/week-07-lecture.md)
- [S3 Security Best Practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)
- [Architecting for HIPAA on AWS](https://docs.aws.amazon.com/whitepapers/latest/architecting-hipaa-security-and-compliance-on-aws/welcome.html)
- [Lake Formation Permissions](https://docs.aws.amazon.com/lake-formation/latest/dg/lake-formation-permissions.html)

## Previous Module

← [Module 6 – Orchestration](../module-06-orchestration/README.md)

## Next Module

→ [Module 8 – Monitoring, Cost Optimization & Operations](../module-08-monitoring-ops/README.md)
