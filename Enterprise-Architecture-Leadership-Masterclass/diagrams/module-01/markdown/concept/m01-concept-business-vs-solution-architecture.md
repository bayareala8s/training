# Business vs Solution Architecture

| Field | Value |
| ----- | ----- |
| ID | `m01-concept-business-vs-solution-architecture` |
| Category | `concept` |
| Module | `module-01` |
| Lesson | 1.1 |
| Lab | — |
| Learning objective | Contrast EA leadership with solution delivery architecture |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-01/mermaid/concept/m01-concept-business-vs-solution-architecture.mmd`](module-01/mermaid/concept/m01-concept-business-vs-solution-architecture.mmd)
- Draw.io: [`module-01/drawio/concept/m01-concept-business-vs-solution-architecture.drawio`](module-01/drawio/concept/m01-concept-business-vs-solution-architecture.drawio)
- SVG: [`module-01/svg/concept/m01-concept-business-vs-solution-architecture.svg`](module-01/svg/concept/m01-concept-business-vs-solution-architecture.svg)
- PNG: [`module-01/png/concept/m01-concept-business-vs-solution-architecture.png`](module-01/png/concept/m01-concept-business-vs-solution-architecture.png)

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
  subgraph EA["Enterprise Architect"]
    E1["Strategy → Priorities"]
    E2["Cross-domain trade-offs"]
    E3["Standards & governance"]
  end
  subgraph SA["Solution Architect"]
    S1["Product / project scope"]
    S2["Design within guardrails"]
    S3["Delivery enablement"]
  end
  EA -->|"Guardrails & ADRs"| SA
  SA -->|"Patterns & feedback"| EA
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
