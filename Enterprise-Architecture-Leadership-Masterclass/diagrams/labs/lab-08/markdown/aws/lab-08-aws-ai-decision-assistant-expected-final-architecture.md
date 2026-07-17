# AI Decision Assistant — Expected Final Architecture

| Field | Value |
| ----- | ----- |
| ID | `lab-08-aws-ai-decision-assistant-expected-final-architecture` |
| Category | `aws` |
| Module | `lab-08` |
| Lesson | — |
| Lab | lab-08 |
| Learning objective | Lab 8 visual: Expected Final Architecture |
| AWS icons | Amazon Bedrock, AWS Lambda, AWS Step Functions, Amazon DynamoDB, Amazon API Gateway, Amazon CloudWatch |

## Formats

- Mermaid: [`labs/lab-08/mermaid/aws/lab-08-aws-ai-decision-assistant-expected-final-architecture.mmd`](labs/lab-08/mermaid/aws/lab-08-aws-ai-decision-assistant-expected-final-architecture.mmd)
- Draw.io: [`labs/lab-08/drawio/aws/lab-08-aws-ai-decision-assistant-expected-final-architecture.drawio`](labs/lab-08/drawio/aws/lab-08-aws-ai-decision-assistant-expected-final-architecture.drawio)
- SVG: [`labs/lab-08/svg/aws/lab-08-aws-ai-decision-assistant-expected-final-architecture.svg`](labs/lab-08/svg/aws/lab-08-aws-ai-decision-assistant-expected-final-architecture.svg)
- PNG: [`labs/lab-08/png/aws/lab-08-aws-ai-decision-assistant-expected-final-architecture.png`](labs/lab-08/png/aws/lab-08-aws-ai-decision-assistant-expected-final-architecture.png)

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
  API --> L --> Bedrock
  L --> Rules --> SF
  L --> DDB
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
