# CloudWatch Alarms Loop

| Field | Value |
| ----- | ----- |
| ID | `m07-security-cloudwatch-alarms-loop` |
| Category | `security` |
| Module | `module-07` |
| Lesson | 7.1 |
| Lab | lab-07 |
| Learning objective | Security/resilience: CloudWatch Alarms Loop |
| AWS icons | Amazon CloudWatch, Amazon SNS |

## Formats

- Mermaid: [`module-07/mermaid/security/m07-security-cloudwatch-alarms-loop.mmd`](module-07/mermaid/security/m07-security-cloudwatch-alarms-loop.mmd)
- Draw.io: [`module-07/drawio/security/m07-security-cloudwatch-alarms-loop.drawio`](module-07/drawio/security/m07-security-cloudwatch-alarms-loop.drawio)
- SVG: [`module-07/svg/security/m07-security-cloudwatch-alarms-loop.svg`](module-07/svg/security/m07-security-cloudwatch-alarms-loop.svg)
- PNG: [`module-07/png/security/m07-security-cloudwatch-alarms-loop.png`](module-07/png/security/m07-security-cloudwatch-alarms-loop.png)

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
  Metric["Metric"] --> Alarm["CloudWatch Alarm"]
  Alarm --> SNS["SNS"]
  SNS --> OnCall["Responder"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
