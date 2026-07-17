# Integration Platform — Security

| Field | Value |
| ----- | ----- |
| ID | `lab-06-security-integration-platform-security` |
| Category | `security` |
| Module | `lab-06` |
| Lesson | — |
| Lab | lab-06 |
| Learning objective | Lab 6 visual: Security |
| AWS icons | Amazon API Gateway, AWS Lambda, Amazon EventBridge, Amazon SQS, AWS Step Functions, Amazon S3, Amazon DynamoDB, Amazon SNS |

## Formats

- Mermaid: [`labs/lab-06/mermaid/security/lab-06-security-integration-platform-security.mmd`](labs/lab-06/mermaid/security/lab-06-security-integration-platform-security.mmd)
- Draw.io: [`labs/lab-06/drawio/security/lab-06-security-integration-platform-security.drawio`](labs/lab-06/drawio/security/lab-06-security-integration-platform-security.drawio)
- SVG: [`labs/lab-06/svg/security/lab-06-security-integration-platform-security.svg`](labs/lab-06/svg/security/lab-06-security-integration-platform-security.svg)
- PNG: [`labs/lab-06/png/security/lab-06-security-integration-platform-security.png`](labs/lab-06/png/security/lab-06-security-integration-platform-security.png)

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
