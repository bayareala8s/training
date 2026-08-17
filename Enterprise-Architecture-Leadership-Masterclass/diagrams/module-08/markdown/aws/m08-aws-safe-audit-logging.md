# Safe Audit Logging

| Field | Value |
| ----- | ----- |
| ID | `m08-aws-safe-audit-logging` |
| Category | `aws` |
| Module | `module-08` |
| Lesson | 8.3 |
| Lab | lab-08 |
| Learning objective | AI strategy: Safe Audit Logging |
| AWS icons | Amazon DynamoDB, Amazon S3 |

## Formats

- Mermaid: [`module-08/mermaid/aws/m08-aws-safe-audit-logging.mmd`](module-08/mermaid/aws/m08-aws-safe-audit-logging.mmd)
- Draw.io: [`module-08/drawio/aws/m08-aws-safe-audit-logging.drawio`](module-08/drawio/aws/m08-aws-safe-audit-logging.drawio)
- SVG: [`module-08/svg/aws/m08-aws-safe-audit-logging.svg`](module-08/svg/aws/m08-aws-safe-audit-logging.svg)
- PNG: [`module-08/png/aws/m08-aws-safe-audit-logging.png`](module-08/png/aws/m08-aws-safe-audit-logging.png)

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
  IO["Inputs/Outputs"] --> Redact["Redact Sensitive"]
  Redact --> Log["Audit Store"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
