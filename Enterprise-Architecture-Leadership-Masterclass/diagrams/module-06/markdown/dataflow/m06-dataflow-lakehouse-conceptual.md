# Lakehouse Conceptual

| Field | Value |
| ----- | ----- |
| ID | `m06-dataflow-lakehouse-conceptual` |
| Category | `dataflow` |
| Module | `module-06` |
| Lesson | 6.1 |
| Lab | lab-06 |
| Learning objective | Integration/data architecture: Lakehouse Conceptual |
| AWS icons | Amazon S3, AWS Glue, Amazon Athena |

## Formats

- Mermaid: [`module-06/mermaid/dataflow/m06-dataflow-lakehouse-conceptual.mmd`](module-06/mermaid/dataflow/m06-dataflow-lakehouse-conceptual.mmd)
- Draw.io: [`module-06/drawio/dataflow/m06-dataflow-lakehouse-conceptual.drawio`](module-06/drawio/dataflow/m06-dataflow-lakehouse-conceptual.drawio)
- SVG: [`module-06/svg/dataflow/m06-dataflow-lakehouse-conceptual.svg`](module-06/svg/dataflow/m06-dataflow-lakehouse-conceptual.svg)
- PNG: [`module-06/png/dataflow/m06-dataflow-lakehouse-conceptual.png`](module-06/png/dataflow/m06-dataflow-lakehouse-conceptual.png)

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
  Src["Sources"] --> S3["S3 Lake"]
  S3 --> Glue["Glue Catalog"]
  Glue --> Athena["Athena / Analytics"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
