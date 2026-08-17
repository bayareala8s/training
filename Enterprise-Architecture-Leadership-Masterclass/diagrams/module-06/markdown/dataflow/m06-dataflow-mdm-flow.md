# MDM Flow

| Field | Value |
| ----- | ----- |
| ID | `m06-dataflow-mdm-flow` |
| Category | `dataflow` |
| Module | `module-06` |
| Lesson | 6.2 |
| Lab | lab-06 |
| Learning objective | Integration/data architecture: MDM Flow |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-06/mermaid/dataflow/m06-dataflow-mdm-flow.mmd`](module-06/mermaid/dataflow/m06-dataflow-mdm-flow.mmd)
- Draw.io: [`module-06/drawio/dataflow/m06-dataflow-mdm-flow.drawio`](module-06/drawio/dataflow/m06-dataflow-mdm-flow.drawio)
- SVG: [`module-06/svg/dataflow/m06-dataflow-mdm-flow.svg`](module-06/svg/dataflow/m06-dataflow-mdm-flow.svg)
- PNG: [`module-06/png/dataflow/m06-dataflow-mdm-flow.png`](module-06/png/dataflow/m06-dataflow-mdm-flow.png)

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
  Sys["Source Systems"] --> MDM["Master Data Services"]
  MDM --> Gold["Golden Record"]
  Gold --> Cons["Downstream"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
