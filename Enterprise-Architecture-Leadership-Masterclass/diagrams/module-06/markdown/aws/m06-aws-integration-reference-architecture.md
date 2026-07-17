# Integration Reference Architecture

| Field | Value |
| ----- | ----- |
| ID | `m06-aws-integration-reference-architecture` |
| Category | `aws` |
| Module | `module-06` |
| Lesson | 6.1 |
| Lab | lab-06 |
| Learning objective | Integration/data architecture: Integration Reference Architecture |
| AWS icons | Amazon API Gateway, AWS Lambda, Amazon EventBridge, Amazon SQS, AWS Step Functions, Amazon S3, Amazon DynamoDB, Amazon SNS |

## Formats

- Mermaid: [`module-06/mermaid/aws/m06-aws-integration-reference-architecture.mmd`](module-06/mermaid/aws/m06-aws-integration-reference-architecture.mmd)
- Draw.io: [`module-06/drawio/aws/m06-aws-integration-reference-architecture.drawio`](module-06/drawio/aws/m06-aws-integration-reference-architecture.drawio)
- SVG: [`module-06/svg/aws/m06-aws-integration-reference-architecture.svg`](module-06/svg/aws/m06-aws-integration-reference-architecture.svg)
- PNG: [`module-06/png/aws/m06-aws-integration-reference-architecture.png`](module-06/png/aws/m06-aws-integration-reference-architecture.png)

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
  Clients["Clients / Partners"] --> APIGW["Amazon API Gateway"]
  APIGW --> Lapi["AWS Lambda — API"]
  Lapi --> EB["Amazon EventBridge"]
  EB --> SQS["Amazon SQS"]
  SQS --> Lproc["AWS Lambda — Processors"]
  Lproc --> DDB["Amazon DynamoDB"]
  S3["Amazon S3 Batches"] --> SF["AWS Step Functions"]
  SF --> Lval["Validate / Route"]
  Lproc --> SNS["Amazon SNS Notify"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
