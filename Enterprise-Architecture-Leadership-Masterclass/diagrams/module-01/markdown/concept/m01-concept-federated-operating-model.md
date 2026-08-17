# Federated Operating Model

| Field | Value |
| ----- | ----- |
| ID | `m01-concept-federated-operating-model` |
| Category | `concept` |
| Module | `module-01` |
| Lesson | 1.2 |
| Lab | — |
| Learning objective | Illustrate Year-1 hybrid/federated EA operating model |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-01/mermaid/concept/m01-concept-federated-operating-model.mmd`](module-01/mermaid/concept/m01-concept-federated-operating-model.mmd)
- Draw.io: [`module-01/drawio/concept/m01-concept-federated-operating-model.drawio`](module-01/drawio/concept/m01-concept-federated-operating-model.drawio)
- SVG: [`module-01/svg/concept/m01-concept-federated-operating-model.svg`](module-01/svg/concept/m01-concept-federated-operating-model.svg)
- PNG: [`module-01/png/concept/m01-concept-federated-operating-model.png`](module-01/png/concept/m01-concept-federated-operating-model.png)

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
flowchart TB
  subgraph Center["Enterprise Architecture Center"]
    EA["Lead EA"]
    Std["Standards · ADRs · ARB"]
  end
  subgraph BUs["Business Units"]
    DA1["Domain Arch — Payments"]
    DA2["Domain Arch — Retail"]
    DA3["Domain Arch — Partners"]
  end
  subgraph Plat["Platform"]
    PA["Platform Architect"]
    GP["Golden Paths"]
  end
  Center --> BUs & Plat
  BUs --> SA["Solution Architects"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
