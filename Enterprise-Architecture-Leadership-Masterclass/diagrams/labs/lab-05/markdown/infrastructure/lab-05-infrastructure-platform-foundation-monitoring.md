# Platform Foundation — Monitoring

| Field | Value |
| ----- | ----- |
| ID | `lab-05-infrastructure-platform-foundation-monitoring` |
| Category | `infrastructure` |
| Module | `lab-05` |
| Lesson | — |
| Lab | lab-05 |
| Learning objective | Lab 5 visual: Monitoring |
| AWS icons | IAM, Amazon S3, AWS CloudTrail, Amazon CloudWatch, AWS Budgets, Amazon DynamoDB, AWS Lambda, Amazon API Gateway, AWS Systems Manager |

## Formats

- Mermaid: [`labs/lab-05/mermaid/infrastructure/lab-05-infrastructure-platform-foundation-monitoring.mmd`](labs/lab-05/mermaid/infrastructure/lab-05-infrastructure-platform-foundation-monitoring.mmd)
- Draw.io: [`labs/lab-05/drawio/infrastructure/lab-05-infrastructure-platform-foundation-monitoring.drawio`](labs/lab-05/drawio/infrastructure/lab-05-infrastructure-platform-foundation-monitoring.drawio)
- SVG: [`labs/lab-05/svg/infrastructure/lab-05-infrastructure-platform-foundation-monitoring.svg`](labs/lab-05/svg/infrastructure/lab-05-infrastructure-platform-foundation-monitoring.svg)
- PNG: [`labs/lab-05/png/infrastructure/lab-05-infrastructure-platform-foundation-monitoring.png`](labs/lab-05/png/infrastructure/lab-05-infrastructure-platform-foundation-monitoring.png)

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
