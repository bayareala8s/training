# Federated vs Centralized

| Field | Value |
| ----- | ----- |
| ID | `m09-concept-federated-vs-centralized` |
| Category | `concept` |
| Module | `module-09` |
| Lesson | 9.3 |
| Lab | lab-09 |
| Learning objective | Governance: Federated vs Centralized |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-09/mermaid/concept/m09-concept-federated-vs-centralized.mmd`](module-09/mermaid/concept/m09-concept-federated-vs-centralized.mmd)
- Draw.io: [`module-09/drawio/concept/m09-concept-federated-vs-centralized.drawio`](module-09/drawio/concept/m09-concept-federated-vs-centralized.drawio)
- SVG: [`module-09/svg/concept/m09-concept-federated-vs-centralized.svg`](module-09/svg/concept/m09-concept-federated-vs-centralized.svg)
- PNG: [`module-09/png/concept/m09-concept-federated-vs-centralized.png`](module-09/png/concept/m09-concept-federated-vs-centralized.png)

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
  Cent["Centralized"] --- Fed["Federated"]
  Cent --> Fit1["High risk standardization"]
  Fed --> Fit2["Domain speed + guardrails"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
