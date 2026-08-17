# Architecture Pyramid

| Field | Value |
| ----- | ----- |
| ID | `m01-concept-architecture-pyramid` |
| Category | `concept` |
| Module | `module-01` |
| Lesson | 1.1 |
| Lab | — |
| Learning objective | Distinguish strategic, segment, and solution architecture |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-01/mermaid/concept/m01-concept-architecture-pyramid.mmd`](module-01/mermaid/concept/m01-concept-architecture-pyramid.mmd)
- Draw.io: [`module-01/drawio/concept/m01-concept-architecture-pyramid.drawio`](module-01/drawio/concept/m01-concept-architecture-pyramid.drawio)
- SVG: [`module-01/svg/concept/m01-concept-architecture-pyramid.svg`](module-01/svg/concept/m01-concept-architecture-pyramid.svg)
- PNG: [`module-01/png/concept/m01-concept-architecture-pyramid.png`](module-01/png/concept/m01-concept-architecture-pyramid.png)

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
  Strat["Strategic Architecture<br/>Enterprise direction"] --> Seg["Segment / Domain Architecture"]
  Seg --> Sol["Solution Architecture"]
  Sol --> Del["Delivery & Engineering"]
  Strat -.-> Prin["Principles & Guardrails"]
  Prin -.-> Seg & Sol
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
