# Lab 7 Secure Platform

| Field | Value |
| ----- | ----- |
| ID | `m07-security-lab-7-secure-platform` |
| Category | `security` |
| Module | `module-07` |
| Lesson | 7.1 |
| Lab | lab-07 |
| Learning objective | Security/resilience: Lab 7 Secure Platform |
| AWS icons | IAM, AWS KMS, Amazon S3, Amazon CloudWatch |

## Formats

- Mermaid: [`module-07/mermaid/security/m07-security-lab-7-secure-platform.mmd`](module-07/mermaid/security/m07-security-lab-7-secure-platform.mmd)
- Draw.io: [`module-07/drawio/security/m07-security-lab-7-secure-platform.drawio`](module-07/drawio/security/m07-security-lab-7-secure-platform.drawio)
- SVG: [`module-07/svg/security/m07-security-lab-7-secure-platform.svg`](module-07/svg/security/m07-security-lab-7-secure-platform.svg)
- PNG: [`module-07/png/security/m07-security-lab-7-secure-platform.png`](module-07/png/security/m07-security-lab-7-secure-platform.png)

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
  subgraph Lab7
    IAM --> App
    App --> KMS
    App --> S3v["S3 Versioned"]
    CW["CloudWatch Alarms"]
  end
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
