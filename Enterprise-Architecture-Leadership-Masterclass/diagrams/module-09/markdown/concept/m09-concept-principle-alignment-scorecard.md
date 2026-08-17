# Principle Alignment Scorecard

| Field | Value |
| ----- | ----- |
| ID | `m09-concept-principle-alignment-scorecard` |
| Category | `concept` |
| Module | `module-09` |
| Lesson | 9.4 |
| Lab | lab-09 |
| Learning objective | Governance: Principle Alignment Scorecard |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-09/mermaid/concept/m09-concept-principle-alignment-scorecard.mmd`](module-09/mermaid/concept/m09-concept-principle-alignment-scorecard.mmd)
- Draw.io: [`module-09/drawio/concept/m09-concept-principle-alignment-scorecard.drawio`](module-09/drawio/concept/m09-concept-principle-alignment-scorecard.drawio)
- SVG: [`module-09/svg/concept/m09-concept-principle-alignment-scorecard.svg`](module-09/svg/concept/m09-concept-principle-alignment-scorecard.svg)
- PNG: [`module-09/png/concept/m09-concept-principle-alignment-scorecard.png`](module-09/png/concept/m09-concept-principle-alignment-scorecard.png)

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
  P1["Principle"] --> Align{"Aligns?"}
  Align -->|No| Risk["Document Risk"]
  Align -->|Yes| Proceed["Proceed"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
