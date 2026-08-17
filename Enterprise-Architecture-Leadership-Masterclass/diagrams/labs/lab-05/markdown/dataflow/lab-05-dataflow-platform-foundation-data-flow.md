# Platform Foundation — Data Flow

| Field | Value |
| ----- | ----- |
| ID | `lab-05-dataflow-platform-foundation-data-flow` |
| Category | `dataflow` |
| Module | `lab-05` |
| Lesson | — |
| Lab | lab-05 |
| Learning objective | Lab 5 visual: Data Flow |
| AWS icons | IAM, Amazon S3, AWS CloudTrail, Amazon CloudWatch, AWS Budgets, Amazon DynamoDB, AWS Lambda, Amazon API Gateway, AWS Systems Manager |

## Formats

- Mermaid: [`labs/lab-05/mermaid/dataflow/lab-05-dataflow-platform-foundation-data-flow.mmd`](labs/lab-05/mermaid/dataflow/lab-05-dataflow-platform-foundation-data-flow.mmd)
- Draw.io: [`labs/lab-05/drawio/dataflow/lab-05-dataflow-platform-foundation-data-flow.drawio`](labs/lab-05/drawio/dataflow/lab-05-dataflow-platform-foundation-data-flow.drawio)
- SVG: [`labs/lab-05/svg/dataflow/lab-05-dataflow-platform-foundation-data-flow.svg`](labs/lab-05/svg/dataflow/lab-05-dataflow-platform-foundation-data-flow.svg)
- PNG: [`labs/lab-05/png/dataflow/lab-05-dataflow-platform-foundation-data-flow.png`](labs/lab-05/png/dataflow/lab-05-dataflow-platform-foundation-data-flow.png)

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
  In["Input"] --> Proc["Process"] --> Out["Output / Store"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
