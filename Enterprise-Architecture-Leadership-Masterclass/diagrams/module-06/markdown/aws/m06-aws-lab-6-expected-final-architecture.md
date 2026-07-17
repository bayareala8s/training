# Lab 6 Expected Final Architecture

| Field | Value |
| ----- | ----- |
| ID | `m06-aws-lab-6-expected-final-architecture` |
| Category | `aws` |
| Module | `module-06` |
| Lesson | 6.4 |
| Lab | lab-06 |
| Learning objective | Integration/data architecture: Lab 6 Expected Final Architecture |
| AWS icons | Amazon API Gateway, AWS Lambda, Amazon EventBridge, Amazon SQS, AWS Step Functions, Amazon S3, Amazon DynamoDB, Amazon SNS |

## Formats

- Mermaid: [`module-06/mermaid/aws/m06-aws-lab-6-expected-final-architecture.mmd`](module-06/mermaid/aws/m06-aws-lab-6-expected-final-architecture.mmd)
- Draw.io: [`module-06/drawio/aws/m06-aws-lab-6-expected-final-architecture.drawio`](module-06/drawio/aws/m06-aws-lab-6-expected-final-architecture.drawio)
- SVG: [`module-06/svg/aws/m06-aws-lab-6-expected-final-architecture.svg`](module-06/svg/aws/m06-aws-lab-6-expected-final-architecture.svg)
- PNG: [`module-06/png/aws/m06-aws-lab-6-expected-final-architecture.png`](module-06/png/aws/m06-aws-lab-6-expected-final-architecture.png)

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
  subgraph Final["Lab 6 Final"]
    APIGW --> L1
    L1 --> EB
    EB --> SQS --> L2 --> DDB
    S3 --> SF --> L3
    L2 --> SNS
  end
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
