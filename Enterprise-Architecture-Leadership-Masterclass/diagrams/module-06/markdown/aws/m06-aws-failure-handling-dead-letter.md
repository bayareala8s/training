# Failure Handling Dead Letter

| Field | Value |
| ----- | ----- |
| ID | `m06-aws-failure-handling-dead-letter` |
| Category | `aws` |
| Module | `module-06` |
| Lesson | 6.3 |
| Lab | lab-06 |
| Learning objective | Integration/data architecture: Failure Handling Dead Letter |
| AWS icons | Amazon SQS, Amazon CloudWatch |

## Formats

- Mermaid: [`module-06/mermaid/aws/m06-aws-failure-handling-dead-letter.mmd`](module-06/mermaid/aws/m06-aws-failure-handling-dead-letter.mmd)
- Draw.io: [`module-06/drawio/aws/m06-aws-failure-handling-dead-letter.drawio`](module-06/drawio/aws/m06-aws-failure-handling-dead-letter.drawio)
- SVG: [`module-06/svg/aws/m06-aws-failure-handling-dead-letter.svg`](module-06/svg/aws/m06-aws-failure-handling-dead-letter.svg)
- PNG: [`module-06/png/aws/m06-aws-failure-handling-dead-letter.png`](module-06/png/aws/m06-aws-failure-handling-dead-letter.png)

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
  Q["SQS"] --> L["Lambda"]
  L -->|fail| DLQ["DLQ"]
  DLQ --> Alarm["CloudWatch Alarm"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
