# Platform Foundation — Security

| Field | Value |
| ----- | ----- |
| ID | `lab-05-security-platform-foundation-security` |
| Category | `security` |
| Module | `lab-05` |
| Lesson | — |
| Lab | lab-05 |
| Learning objective | Lab 5 visual: Security |
| AWS icons | IAM, Amazon S3, AWS CloudTrail, Amazon CloudWatch, AWS Budgets, Amazon DynamoDB, AWS Lambda, Amazon API Gateway, AWS Systems Manager |

## Formats

- Mermaid: [`labs/lab-05/mermaid/security/lab-05-security-platform-foundation-security.mmd`](labs/lab-05/mermaid/security/lab-05-security-platform-foundation-security.mmd)
- Draw.io: [`labs/lab-05/drawio/security/lab-05-security-platform-foundation-security.drawio`](labs/lab-05/drawio/security/lab-05-security-platform-foundation-security.drawio)
- SVG: [`labs/lab-05/svg/security/lab-05-security-platform-foundation-security.svg`](labs/lab-05/svg/security/lab-05-security-platform-foundation-security.svg)
- PNG: [`labs/lab-05/png/security/lab-05-security-platform-foundation-security.png`](labs/lab-05/png/security/lab-05-security-platform-foundation-security.png)

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
