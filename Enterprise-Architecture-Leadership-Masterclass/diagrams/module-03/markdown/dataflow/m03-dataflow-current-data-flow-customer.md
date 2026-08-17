# Current Data Flow Customer

| Field | Value |
| ----- | ----- |
| ID | `m03-dataflow-current-data-flow-customer` |
| Category | `dataflow` |
| Module | `module-03` |
| Lesson | 3.2 |
| Lab | lab-03 |
| Learning objective | Assess current estate: Current Data Flow Customer |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-03/mermaid/dataflow/m03-dataflow-current-data-flow-customer.mmd`](module-03/mermaid/dataflow/m03-dataflow-current-data-flow-customer.mmd)
- Draw.io: [`module-03/drawio/dataflow/m03-dataflow-current-data-flow-customer.drawio`](module-03/drawio/dataflow/m03-dataflow-current-data-flow-customer.drawio)
- SVG: [`module-03/svg/dataflow/m03-dataflow-current-data-flow-customer.svg`](module-03/svg/dataflow/m03-dataflow-current-data-flow-customer.svg)
- PNG: [`module-03/png/dataflow/m03-dataflow-current-data-flow-customer.png`](module-03/png/dataflow/m03-dataflow-current-data-flow-customer.png)

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
  Web["Web Portal"] --> CRM["CallCenter CRM"]
  Mobile["Mobile BFF"] --> CRM
  CRM --> C360["Cust360 MDM"]
  C360 --> Replica["Cust360 Replica EU"]
  C360 --> Lake["DataLake Alpha"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
