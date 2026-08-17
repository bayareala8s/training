# Technologies and prerequisites

## Prerequisites checklist

| Skill | Expected level |
|-------|----------------|
| AWS Console & CLI | Comfortable creating S3, IAM roles, Lambda |
| Networking | Understand subnets, security groups, NAT (week 2+) |
| Identity | IAM users/roles/policies; optional OIDC/SAML awareness |
| Scripting | Read/modify Python or Node Lambda samples |
| IaC | Follow Terraform apply/plan (solutions provided as reference) |
| Git | Clone, branch, commit capstone artifacts |

## AWS services by week

| Service | Weeks | Role in course |
|---------|-------|----------------|
| **AWS Transfer Family** | 1, 2, 5 | SFTP server, managed users, connectors |
| **Amazon S3** | 1–8 | Landing zones, artifacts, audit exports |
| **IAM** | 1–8 | Least privilege, trust policies for Transfer |
| **AWS KMS** | 2, 4–8 | Encryption at rest, key policies |
| **Amazon VPC** | 2, 5 | Endpoint placement, connector egress |
| **AWS Lambda** | 3–8 | Event processing, API backends |
| **AWS Step Functions** | 4–8 | Orchestration, retries, human gates |
| **Amazon EventBridge** | 3–4 | S3/event routing |
| **Amazon DynamoDB** | 6–8 | Connection catalog, job state |
| **Amazon API Gateway** | 6–8 | REST APIs for self-serve |
| **Amazon Cognito** | 6–8 | User pools, hosted UI patterns |
| **Amazon CloudWatch** | 3–8 | Logs, metrics, alarms |
| **AWS CloudTrail** | 2, 7 | Audit and compliance evidence |
| **Amazon SNS / SQS** | 4 (optional) | Notifications, DLQ patterns |
| **Terraform** | 2–8 | IaC labs and capstone skeleton |

## Stretch technologies (optional)

| Service | When | Notes |
|---------|------|-------|
| Amazon Bedrock Agents | Week 8 stretch | Natural-language ops queries; policy-bound |
| OpenSearch Serverless | Week 8 stretch | RAG over runbooks and partner docs |
| Amazon ECS Fargate | **Lab 9** (Week 5+) | Long-running / large-file workers — [lab guide](labs/lab-09-ecs-fargate-large-files.md) |
| AWS Secrets Manager | 2, 5 | Partner credentials; never in code |

## Local tooling

- AWS CLI v2  
- Terraform ≥ 1.5  
- Python 3.11+ or Node 20+ (match Lambda runtime in labs)  
- `jq`, `curl`, SFTP client (`sftp`, FileZilla, or `lftp`)  
- Postman or HTTPie for API labs  

## Sandbox requirements

- Dedicated AWS account or sub-account with **$50–150/month** budget guidance  
- Region: **us-east-1** or **us-west-2** (labs written for either; stay consistent)  
- **Billing alarm** at $25, $50, $100  
- Tag resources: `Project=BayLearn-MFT`, `Owner=<email>`  

## Reference documentation

- [AWS Transfer Family User Guide](https://docs.aws.amazon.com/transfer/latest/userguide/what-is-aws-transfer-family.html)  
- [Transfer Family IAM requirements](https://docs.aws.amazon.com/transfer/latest/userguide/requirements-roles.html)  
- [S3 security best practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)  
- [Step Functions error handling](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html)  

## Cost management tips

- Stop Transfer Family servers when not in lab (`enable_transfer_family = false` in Terraform patterns).  
- Use S3 lifecycle rules on lab prefixes.  
- Destroy capstone resources after demo recording.  
