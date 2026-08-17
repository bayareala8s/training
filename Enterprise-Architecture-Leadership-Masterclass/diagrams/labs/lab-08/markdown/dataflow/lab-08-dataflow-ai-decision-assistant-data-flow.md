# AI Decision Assistant — Data Flow

| Field | Value |
| ----- | ----- |
| ID | `lab-08-dataflow-ai-decision-assistant-data-flow` |
| Category | `dataflow` |
| Module | `lab-08` |
| Lesson | — |
| Lab | lab-08 |
| Learning objective | Lab 8 visual: Data Flow |
| AWS icons | Amazon Bedrock, AWS Lambda, AWS Step Functions, Amazon DynamoDB, Amazon API Gateway, Amazon CloudWatch |

## Formats

- Mermaid: [`labs/lab-08/mermaid/dataflow/lab-08-dataflow-ai-decision-assistant-data-flow.mmd`](labs/lab-08/mermaid/dataflow/lab-08-dataflow-ai-decision-assistant-data-flow.mmd)
- Draw.io: [`labs/lab-08/drawio/dataflow/lab-08-dataflow-ai-decision-assistant-data-flow.drawio`](labs/lab-08/drawio/dataflow/lab-08-dataflow-ai-decision-assistant-data-flow.drawio)
- SVG: [`labs/lab-08/svg/dataflow/lab-08-dataflow-ai-decision-assistant-data-flow.svg`](labs/lab-08/svg/dataflow/lab-08-dataflow-ai-decision-assistant-data-flow.svg)
- PNG: [`labs/lab-08/png/dataflow/lab-08-dataflow-ai-decision-assistant-data-flow.png`](labs/lab-08/png/dataflow/lab-08-dataflow-ai-decision-assistant-data-flow.png)

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
