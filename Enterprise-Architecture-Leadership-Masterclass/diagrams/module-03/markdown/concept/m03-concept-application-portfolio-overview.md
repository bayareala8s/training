# Application Portfolio Overview

| Field | Value |
| ----- | ----- |
| ID | `m03-concept-application-portfolio-overview` |
| Category | `concept` |
| Module | `module-03` |
| Lesson | 3.1 |
| Lab | lab-03 |
| Learning objective | Assess current estate: Application Portfolio Overview |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-03/mermaid/concept/m03-concept-application-portfolio-overview.mmd`](module-03/mermaid/concept/m03-concept-application-portfolio-overview.mmd)
- Draw.io: [`module-03/drawio/concept/m03-concept-application-portfolio-overview.drawio`](module-03/drawio/concept/m03-concept-application-portfolio-overview.drawio)
- SVG: [`module-03/svg/concept/m03-concept-application-portfolio-overview.svg`](module-03/svg/concept/m03-concept-application-portfolio-overview.svg)
- PNG: [`module-03/png/concept/m03-concept-application-portfolio-overview.png`](module-03/png/concept/m03-concept-application-portfolio-overview.png)

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
  Inv["Application Inventory 50+"] --> Score["Value × Health"]
  Score --> TIME["TIME Disposition"]
  TIME --> Heat["Portfolio Heatmap"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
