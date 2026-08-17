# Integration Platform — Monitoring

| Field | Value |
| ----- | ----- |
| ID | `lab-06-infrastructure-integration-platform-monitoring` |
| Category | `infrastructure` |
| Module | `lab-06` |
| Lesson | — |
| Lab | lab-06 |
| Learning objective | Lab 6 visual: Monitoring |
| AWS icons | Amazon API Gateway, AWS Lambda, Amazon EventBridge, Amazon SQS, AWS Step Functions, Amazon S3, Amazon DynamoDB, Amazon SNS |

## Formats

- Mermaid: [`labs/lab-06/mermaid/infrastructure/lab-06-infrastructure-integration-platform-monitoring.mmd`](labs/lab-06/mermaid/infrastructure/lab-06-infrastructure-integration-platform-monitoring.mmd)
- Draw.io: [`labs/lab-06/drawio/infrastructure/lab-06-infrastructure-integration-platform-monitoring.drawio`](labs/lab-06/drawio/infrastructure/lab-06-infrastructure-integration-platform-monitoring.drawio)
- SVG: [`labs/lab-06/svg/infrastructure/lab-06-infrastructure-integration-platform-monitoring.svg`](labs/lab-06/svg/infrastructure/lab-06-infrastructure-integration-platform-monitoring.svg)
- PNG: [`labs/lab-06/png/infrastructure/lab-06-infrastructure-integration-platform-monitoring.png`](labs/lab-06/png/infrastructure/lab-06-infrastructure-integration-platform-monitoring.png)

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
  Metrics --> Alarms --> Notify
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
