# Integration Sprawl Current

| Field | Value |
| ----- | ----- |
| ID | `m03-dataflow-integration-sprawl-current` |
| Category | `dataflow` |
| Module | `module-03` |
| Lesson | 3.1 |
| Lab | lab-03 |
| Learning objective | Assess current estate: Integration Sprawl Current |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-03/mermaid/dataflow/m03-dataflow-integration-sprawl-current.mmd`](module-03/mermaid/dataflow/m03-dataflow-integration-sprawl-current.mmd)
- Draw.io: [`module-03/drawio/dataflow/m03-dataflow-integration-sprawl-current.drawio`](module-03/drawio/dataflow/m03-dataflow-integration-sprawl-current.drawio)
- SVG: [`module-03/svg/dataflow/m03-dataflow-integration-sprawl-current.svg`](module-03/svg/dataflow/m03-dataflow-integration-sprawl-current.svg)
- PNG: [`module-03/png/dataflow/m03-dataflow-integration-sprawl-current.png`](module-03/png/dataflow/m03-dataflow-integration-sprawl-current.png)

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
  A1["App A"] -->|Point-to-point| A2["App B"]
  A1 -->|Files| SFTP1["SFTP Hub East"]
  A2 -->|Files| SFTP2["SFTP Hub West"]
  A3["App C"] -->|DB Link| A4["App D"]
  A1 -->|API ad-hoc| A5["App E"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
