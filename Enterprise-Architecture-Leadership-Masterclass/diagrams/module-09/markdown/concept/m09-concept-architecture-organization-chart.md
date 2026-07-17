# Architecture Organization Chart

| Field | Value |
| ----- | ----- |
| ID | `m09-concept-architecture-organization-chart` |
| Category | `concept` |
| Module | `module-09` |
| Lesson | 9.4 |
| Lab | lab-09 |
| Learning objective | Governance: Architecture Organization Chart |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-09/mermaid/concept/m09-concept-architecture-organization-chart.mmd`](module-09/mermaid/concept/m09-concept-architecture-organization-chart.mmd)
- Draw.io: [`module-09/drawio/concept/m09-concept-architecture-organization-chart.drawio`](module-09/drawio/concept/m09-concept-architecture-organization-chart.drawio)
- SVG: [`module-09/svg/concept/m09-concept-architecture-organization-chart.svg`](module-09/svg/concept/m09-concept-architecture-organization-chart.svg)
- PNG: [`module-09/png/concept/m09-concept-architecture-organization-chart.png`](module-09/png/concept/m09-concept-architecture-organization-chart.png)

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
  CIO --> EA
  EA --> Domain
  EA --> Platform
  EA --> ARB
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
