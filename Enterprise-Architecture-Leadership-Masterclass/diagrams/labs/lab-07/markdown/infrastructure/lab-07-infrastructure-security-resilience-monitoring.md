# Security Resilience — Monitoring

| Field | Value |
| ----- | ----- |
| ID | `lab-07-infrastructure-security-resilience-monitoring` |
| Category | `infrastructure` |
| Module | `lab-07` |
| Lesson | — |
| Lab | lab-07 |
| Learning objective | Lab 7 visual: Monitoring |
| AWS icons | IAM, AWS KMS, Amazon S3, Amazon CloudWatch |

## Formats

- Mermaid: [`labs/lab-07/mermaid/infrastructure/lab-07-infrastructure-security-resilience-monitoring.mmd`](labs/lab-07/mermaid/infrastructure/lab-07-infrastructure-security-resilience-monitoring.mmd)
- Draw.io: [`labs/lab-07/drawio/infrastructure/lab-07-infrastructure-security-resilience-monitoring.drawio`](labs/lab-07/drawio/infrastructure/lab-07-infrastructure-security-resilience-monitoring.drawio)
- SVG: [`labs/lab-07/svg/infrastructure/lab-07-infrastructure-security-resilience-monitoring.svg`](labs/lab-07/svg/infrastructure/lab-07-infrastructure-security-resilience-monitoring.svg)
- PNG: [`labs/lab-07/png/infrastructure/lab-07-infrastructure-security-resilience-monitoring.png`](labs/lab-07/png/infrastructure/lab-07-infrastructure-security-resilience-monitoring.png)

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
