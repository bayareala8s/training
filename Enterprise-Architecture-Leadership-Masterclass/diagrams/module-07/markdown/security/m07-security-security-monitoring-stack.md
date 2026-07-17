# Security Monitoring Stack

| Field | Value |
| ----- | ----- |
| ID | `m07-security-security-monitoring-stack` |
| Category | `security` |
| Module | `module-07` |
| Lesson | 7.4 |
| Lab | lab-07 |
| Learning objective | Security/resilience: Security Monitoring Stack |
| AWS icons | AWS CloudTrail, Amazon CloudWatch, AWS Config |

## Formats

- Mermaid: [`module-07/mermaid/security/m07-security-security-monitoring-stack.mmd`](module-07/mermaid/security/m07-security-security-monitoring-stack.mmd)
- Draw.io: [`module-07/drawio/security/m07-security-security-monitoring-stack.drawio`](module-07/drawio/security/m07-security-security-monitoring-stack.drawio)
- SVG: [`module-07/svg/security/m07-security-security-monitoring-stack.svg`](module-07/svg/security/m07-security-security-monitoring-stack.svg)
- PNG: [`module-07/png/security/m07-security-security-monitoring-stack.png`](module-07/png/security/m07-security-security-monitoring-stack.png)

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
  CT["CloudTrail"] --> SIEM["Detect / Alert"]
  CW["CloudWatch"] --> SIEM
  Config["Config"] --> SIEM
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
