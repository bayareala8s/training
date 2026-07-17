# Prerequisites — Module 07

**Module:** Security, Risk, Compliance, and Resilience

---

## Required prior learning

| Prerequisite | Why it matters |
| ------------ | -------------- |
| Module 01 — EA role and operating model | Security/resilience decisions need clear decision rights |
| Module 03 — Current-state risks | Students reuse NorthStar risk language |
| Module 05 — Cloud/platform foundation | Landing-zone and tagging habits carry forward |
| Module 06 — Integration patterns | Trust boundaries often sit at integration edges |

Students who missed Modules 05–06 should review platform tagging, serverless cost rules, and API/event boundaries before the AWS lab.

---

## Technical prerequisites (lab)

| Tool / capability | Minimum |
| ----------------- | ------- |
| AWS account (sandbox preferred) | Ability to create IAM, KMS, S3, CloudWatch, DynamoDB, SNS, Lambda |
| AWS CLI | v2.x configured with a named profile |
| Terraform | 1.5+ |
| Permissions | Deploy lab resources; create budget alerts |
| Browser | AWS Console for validation screenshots |

---

## Conceptual prerequisites

- Familiarity with IAM roles vs. users
- Basic encryption concepts (at rest vs. in transit)
- Understanding that financial-services controls require *evidence*, not slogans
- Awareness that RTO/RPO are business targets, not purely technical preferences

---

## Cost and safety prerequisites

Before deploying Lab 07:

1. Create or verify an AWS Budget alert (recommended threshold: $10–$25 for the cohort week).
2. Confirm the cleanup script path: `infrastructure/terraform/scripts/cleanup-lab07.sh`.
3. Agree not to use production data or real customer PII.
4. Tag every resource with BayLearn required tags.

---

## Recommended reading (non-proprietary)

- Course templates: threat model, RTO/RPO worksheet, risk-control matrix
- NorthStar case study baseline (`course-specification/northstar-case-study.md`)
- Content standards AWS lab rules (no NAT Gateway, always-on EC2, EKS, OpenSearch)
