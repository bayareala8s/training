# Security Resilience — Data Flow

| Field | Value |
| ----- | ----- |
| ID | `lab-07-dataflow-security-resilience-data-flow` |
| Category | `dataflow` |
| Module | `lab-07` |
| Lesson | — |
| Lab | lab-07 |
| Learning objective | Lab 7 visual: Data Flow |
| AWS icons | IAM, AWS KMS, Amazon S3, Amazon CloudWatch |

## Formats

- Mermaid: [`labs/lab-07/mermaid/dataflow/lab-07-dataflow-security-resilience-data-flow.mmd`](labs/lab-07/mermaid/dataflow/lab-07-dataflow-security-resilience-data-flow.mmd)
- Draw.io: [`labs/lab-07/drawio/dataflow/lab-07-dataflow-security-resilience-data-flow.drawio`](labs/lab-07/drawio/dataflow/lab-07-dataflow-security-resilience-data-flow.drawio)
- SVG: [`labs/lab-07/svg/dataflow/lab-07-dataflow-security-resilience-data-flow.svg`](labs/lab-07/svg/dataflow/lab-07-dataflow-security-resilience-data-flow.svg)
- PNG: [`labs/lab-07/png/dataflow/lab-07-dataflow-security-resilience-data-flow.png`](labs/lab-07/png/dataflow/lab-07-dataflow-security-resilience-data-flow.png)

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
