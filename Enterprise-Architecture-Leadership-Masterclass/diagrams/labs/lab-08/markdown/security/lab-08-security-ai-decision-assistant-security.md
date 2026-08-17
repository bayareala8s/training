# AI Decision Assistant — Security

| Field | Value |
| ----- | ----- |
| ID | `lab-08-security-ai-decision-assistant-security` |
| Category | `security` |
| Module | `lab-08` |
| Lesson | — |
| Lab | lab-08 |
| Learning objective | Lab 8 visual: Security |
| AWS icons | Amazon Bedrock, AWS Lambda, AWS Step Functions, Amazon DynamoDB, Amazon API Gateway, Amazon CloudWatch |

## Formats

- Mermaid: [`labs/lab-08/mermaid/security/lab-08-security-ai-decision-assistant-security.mmd`](labs/lab-08/mermaid/security/lab-08-security-ai-decision-assistant-security.mmd)
- Draw.io: [`labs/lab-08/drawio/security/lab-08-security-ai-decision-assistant-security.drawio`](labs/lab-08/drawio/security/lab-08-security-ai-decision-assistant-security.drawio)
- SVG: [`labs/lab-08/svg/security/lab-08-security-ai-decision-assistant-security.svg`](labs/lab-08/svg/security/lab-08-security-ai-decision-assistant-security.svg)
- PNG: [`labs/lab-08/png/security/lab-08-security-ai-decision-assistant-security.png`](labs/lab-08/png/security/lab-08-security-ai-decision-assistant-security.png)

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
