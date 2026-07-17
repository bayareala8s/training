# Security Resilience — Security

| Field | Value |
| ----- | ----- |
| ID | `lab-07-security-security-resilience-security` |
| Category | `security` |
| Module | `lab-07` |
| Lesson | — |
| Lab | lab-07 |
| Learning objective | Lab 7 visual: Security |
| AWS icons | IAM, AWS KMS, Amazon S3, Amazon CloudWatch |

## Formats

- Mermaid: [`labs/lab-07/mermaid/security/lab-07-security-security-resilience-security.mmd`](labs/lab-07/mermaid/security/lab-07-security-security-resilience-security.mmd)
- Draw.io: [`labs/lab-07/drawio/security/lab-07-security-security-resilience-security.drawio`](labs/lab-07/drawio/security/lab-07-security-security-resilience-security.drawio)
- SVG: [`labs/lab-07/svg/security/lab-07-security-security-resilience-security.svg`](labs/lab-07/svg/security/lab-07-security-security-resilience-security.svg)
- PNG: [`labs/lab-07/png/security/lab-07-security-security-resilience-security.png`](labs/lab-07/png/security/lab-07-security-security-resilience-security.png)

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
  IAM["Least Privilege IAM"] --> Enc["Encryption"]
  Enc --> Audit["Audit Logging"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
