# Decision Hierarchy

| Field | Value |
| ----- | ----- |
| ID | `m01-concept-decision-hierarchy` |
| Category | `concept` |
| Module | `module-01` |
| Lesson | 1.2 |
| Lab | — |
| Learning objective | Clarify local autonomy vs enterprise decisions |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-01/mermaid/concept/m01-concept-decision-hierarchy.mmd`](module-01/mermaid/concept/m01-concept-decision-hierarchy.mmd)
- Draw.io: [`module-01/drawio/concept/m01-concept-decision-hierarchy.drawio`](module-01/drawio/concept/m01-concept-decision-hierarchy.drawio)
- SVG: [`module-01/svg/concept/m01-concept-decision-hierarchy.svg`](module-01/svg/concept/m01-concept-decision-hierarchy.svg)
- PNG: [`module-01/png/concept/m01-concept-decision-hierarchy.png`](module-01/png/concept/m01-concept-decision-hierarchy.png)

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
  E["Enterprise Decisions<br/>Standards · Multi-year · Material risk"] --> D["Domain Decisions"]
  D --> L["Local Solution Decisions<br/>Within guardrails"]
  E --> G["Automated Guardrails"]
  G --> L
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
