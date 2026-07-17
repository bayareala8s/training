# Integration Platform — Target Architecture

| Field | Value |
| ----- | ----- |
| ID | `lab-06-aws-integration-platform-target-architecture` |
| Category | `aws` |
| Module | `lab-06` |
| Lesson | — |
| Lab | lab-06 |
| Learning objective | Lab 6 visual: Target Architecture |
| AWS icons | Amazon API Gateway, AWS Lambda, Amazon EventBridge, Amazon SQS, AWS Step Functions, Amazon S3, Amazon DynamoDB, Amazon SNS |

## Formats

- Mermaid: [`labs/lab-06/mermaid/aws/lab-06-aws-integration-platform-target-architecture.mmd`](labs/lab-06/mermaid/aws/lab-06-aws-integration-platform-target-architecture.mmd)
- Draw.io: [`labs/lab-06/drawio/aws/lab-06-aws-integration-platform-target-architecture.drawio`](labs/lab-06/drawio/aws/lab-06-aws-integration-platform-target-architecture.drawio)
- SVG: [`labs/lab-06/svg/aws/lab-06-aws-integration-platform-target-architecture.svg`](labs/lab-06/svg/aws/lab-06-aws-integration-platform-target-architecture.svg)
- PNG: [`labs/lab-06/png/aws/lab-06-aws-integration-platform-target-architecture.png`](labs/lab-06/png/aws/lab-06-aws-integration-platform-target-architecture.png)

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
flowchart LR
  APIGW --> L --> EB --> SQS --> L2
  S3 --> SF --> L3
  L2 --> SNS
  L2 --> DDB
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
