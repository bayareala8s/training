# Application Ownership Matrix View

| Field | Value |
| ----- | ----- |
| ID | `m03-concept-application-ownership-matrix-view` |
| Category | `concept` |
| Module | `module-03` |
| Lesson | 3.3 |
| Lab | lab-03 |
| Learning objective | Assess current estate: Application Ownership Matrix View |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-03/mermaid/concept/m03-concept-application-ownership-matrix-view.mmd`](module-03/mermaid/concept/m03-concept-application-ownership-matrix-view.mmd)
- Draw.io: [`module-03/drawio/concept/m03-concept-application-ownership-matrix-view.drawio`](module-03/drawio/concept/m03-concept-application-ownership-matrix-view.drawio)
- SVG: [`module-03/svg/concept/m03-concept-application-ownership-matrix-view.svg`](module-03/svg/concept/m03-concept-application-ownership-matrix-view.svg)
- PNG: [`module-03/png/concept/m03-concept-application-ownership-matrix-view.png`](module-03/png/concept/m03-concept-application-ownership-matrix-view.png)

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
  App["Application"] --> BO["Business Owner"]
  App --> TO["Technical Owner"]
  App --> Cap["Primary Capability"]
  App --> Crit["Criticality"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
