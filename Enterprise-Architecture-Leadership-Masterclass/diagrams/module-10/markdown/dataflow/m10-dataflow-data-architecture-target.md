# Data Architecture Target

| Field | Value |
| ----- | ----- |
| ID | `m10-dataflow-data-architecture-target` |
| Category | `dataflow` |
| Module | `module-10` |
| Lesson | 10.1 |
| Lab | lab-10 |
| Learning objective | Capstone visual: Data Architecture Target |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-10/mermaid/dataflow/m10-dataflow-data-architecture-target.mmd`](module-10/mermaid/dataflow/m10-dataflow-data-architecture-target.mmd)
- Draw.io: [`module-10/drawio/dataflow/m10-dataflow-data-architecture-target.drawio`](module-10/drawio/dataflow/m10-dataflow-data-architecture-target.drawio)
- SVG: [`module-10/svg/dataflow/m10-dataflow-data-architecture-target.svg`](module-10/svg/dataflow/m10-dataflow-data-architecture-target.svg)
- PNG: [`module-10/png/dataflow/m10-dataflow-data-architecture-target.png`](module-10/png/dataflow/m10-dataflow-data-architecture-target.png)

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
  Sources --> MDM --> Products --> Consumers
  Sources --> Lakehouse
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
