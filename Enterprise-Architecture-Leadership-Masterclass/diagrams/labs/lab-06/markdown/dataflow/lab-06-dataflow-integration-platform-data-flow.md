# Integration Platform — Data Flow

| Field | Value |
| ----- | ----- |
| ID | `lab-06-dataflow-integration-platform-data-flow` |
| Category | `dataflow` |
| Module | `lab-06` |
| Lesson | — |
| Lab | lab-06 |
| Learning objective | Lab 6 visual: Data Flow |
| AWS icons | Amazon API Gateway, AWS Lambda, Amazon EventBridge, Amazon SQS, AWS Step Functions, Amazon S3, Amazon DynamoDB, Amazon SNS |

## Formats

- Mermaid: [`labs/lab-06/mermaid/dataflow/lab-06-dataflow-integration-platform-data-flow.mmd`](labs/lab-06/mermaid/dataflow/lab-06-dataflow-integration-platform-data-flow.mmd)
- Draw.io: [`labs/lab-06/drawio/dataflow/lab-06-dataflow-integration-platform-data-flow.drawio`](labs/lab-06/drawio/dataflow/lab-06-dataflow-integration-platform-data-flow.drawio)
- SVG: [`labs/lab-06/svg/dataflow/lab-06-dataflow-integration-platform-data-flow.svg`](labs/lab-06/svg/dataflow/lab-06-dataflow-integration-platform-data-flow.svg)
- PNG: [`labs/lab-06/png/dataflow/lab-06-dataflow-integration-platform-data-flow.png`](labs/lab-06/png/dataflow/lab-06-dataflow-integration-platform-data-flow.png)

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
