# Trust Boundaries

| Field | Value |
| ----- | ----- |
| ID | `m07-security-trust-boundaries` |
| Category | `security` |
| Module | `module-07` |
| Lesson | 7.3 |
| Lab | lab-07 |
| Learning objective | Security/resilience: Trust Boundaries |
| AWS icons | Amazon API Gateway, AWS Lambda, Amazon DynamoDB |

## Formats

- Mermaid: [`module-07/mermaid/security/m07-security-trust-boundaries.mmd`](module-07/mermaid/security/m07-security-trust-boundaries.mmd)
- Draw.io: [`module-07/drawio/security/m07-security-trust-boundaries.drawio`](module-07/drawio/security/m07-security-trust-boundaries.drawio)
- SVG: [`module-07/svg/security/m07-security-trust-boundaries.svg`](module-07/svg/security/m07-security-trust-boundaries.svg)
- PNG: [`module-07/png/security/m07-security-trust-boundaries.png`](module-07/png/security/m07-security-trust-boundaries.png)

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
  subgraph Public["Untrusted"]
    Client
  end
  subgraph Edge["Edge Trust"]
    APIGW["API Gateway"]
  end
  subgraph App["App Trust"]
    L["Lambda"]
  end
  subgraph Data["Data Trust"]
    DDB["DynamoDB"]
    KMS["KMS"]
  end
  Client --> APIGW --> L --> DDB
  L --> KMS
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
