# Analytics Pipeline Tap

| Field | Value |
| ----- | ----- |
| ID | `m06-dataflow-analytics-pipeline-tap` |
| Category | `dataflow` |
| Module | `module-06` |
| Lesson | 6.3 |
| Lab | lab-06 |
| Learning objective | Integration/data architecture: Analytics Pipeline Tap |
| AWS icons | Amazon EventBridge, Amazon S3 |

## Formats

- Mermaid: [`module-06/mermaid/dataflow/m06-dataflow-analytics-pipeline-tap.mmd`](module-06/mermaid/dataflow/m06-dataflow-analytics-pipeline-tap.mmd)
- Draw.io: [`module-06/drawio/dataflow/m06-dataflow-analytics-pipeline-tap.drawio`](module-06/drawio/dataflow/m06-dataflow-analytics-pipeline-tap.drawio)
- SVG: [`module-06/svg/dataflow/m06-dataflow-analytics-pipeline-tap.svg`](module-06/svg/dataflow/m06-dataflow-analytics-pipeline-tap.svg)
- PNG: [`module-06/png/dataflow/m06-dataflow-analytics-pipeline-tap.png`](module-06/png/dataflow/m06-dataflow-analytics-pipeline-tap.png)

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
  EB["EventBridge"] --> Firehose["Stream/Buffer"]
  Firehose --> S3["S3 Analytics Zone"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
