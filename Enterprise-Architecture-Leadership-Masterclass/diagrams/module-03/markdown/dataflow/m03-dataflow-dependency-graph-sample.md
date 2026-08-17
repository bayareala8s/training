# Dependency Graph Sample

| Field | Value |
| ----- | ----- |
| ID | `m03-dataflow-dependency-graph-sample` |
| Category | `dataflow` |
| Module | `module-03` |
| Lesson | 3.2 |
| Lab | lab-03 |
| Learning objective | Assess current estate: Dependency Graph Sample |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-03/mermaid/dataflow/m03-dataflow-dependency-graph-sample.mmd`](module-03/mermaid/dataflow/m03-dataflow-dependency-graph-sample.mmd)
- Draw.io: [`module-03/drawio/dataflow/m03-dataflow-dependency-graph-sample.drawio`](module-03/drawio/dataflow/m03-dataflow-dependency-graph-sample.drawio)
- SVG: [`module-03/svg/dataflow/m03-dataflow-dependency-graph-sample.svg`](module-03/svg/dataflow/m03-dataflow-dependency-graph-sample.svg)
- PNG: [`module-03/png/dataflow/m03-dataflow-dependency-graph-sample.png`](module-03/png/dataflow/m03-dataflow-dependency-graph-sample.png)

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
  Pay["PulsePay Gateway"] --> Ledger["LedgerOne"]
  Pay --> Fraud["FraudShield"]
  Orbit["Orbit Onboarding"] --> KYC["KYC Studio"]
  Orbit --> C360["Cust360"]
  Partner["PartnerLink"] --> SFTP["SFTP Hubs"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
