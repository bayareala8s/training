# Platform Foundation — Expected Final Architecture

| Field | Value |
| ----- | ----- |
| ID | `lab-05-aws-platform-foundation-expected-final-architecture` |
| Category | `aws` |
| Module | `lab-05` |
| Lesson | — |
| Lab | lab-05 |
| Learning objective | Lab 5 visual: Expected Final Architecture |
| AWS icons | IAM, Amazon S3, AWS CloudTrail, Amazon CloudWatch, AWS Budgets, Amazon DynamoDB, AWS Lambda, Amazon API Gateway, AWS Systems Manager |

## Formats

- Mermaid: [`labs/lab-05/mermaid/aws/lab-05-aws-platform-foundation-expected-final-architecture.mmd`](labs/lab-05/mermaid/aws/lab-05-aws-platform-foundation-expected-final-architecture.mmd)
- Draw.io: [`labs/lab-05/drawio/aws/lab-05-aws-platform-foundation-expected-final-architecture.drawio`](labs/lab-05/drawio/aws/lab-05-aws-platform-foundation-expected-final-architecture.drawio)
- SVG: [`labs/lab-05/svg/aws/lab-05-aws-platform-foundation-expected-final-architecture.svg`](labs/lab-05/svg/aws/lab-05-aws-platform-foundation-expected-final-architecture.svg)
- PNG: [`labs/lab-05/png/aws/lab-05-aws-platform-foundation-expected-final-architecture.png`](labs/lab-05/png/aws/lab-05-aws-platform-foundation-expected-final-architecture.png)

## Mermaid

```mermaid
%%{init: {
  "theme": "base",
  "themeVariables": {
    "primaryColor": "#E6F2FF",
    "primaryTextColor": "#232F3E",
    "primaryBorderColor": "#146EB4",
    "lineColor": "#545B64",
    "secondaryColor": "#F0F7E6",
    "tertiaryColor": "#FFF3E0",
    "background": "#FFFFFF",
    "fontFamily": "Amazon Ember, Helvetica, Arial, sans-serif"
  }
}}%%
flowchart TB
  APIGW["API Gateway"] --> L["Lambda"]
  L --> DDB["DynamoDB"]
  L --> SSM["SSM"]
  CT["CloudTrail"] --> S3["S3"]
  Bud["Budgets"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
