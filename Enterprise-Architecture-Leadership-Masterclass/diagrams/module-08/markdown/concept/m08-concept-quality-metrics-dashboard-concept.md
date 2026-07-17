# Quality Metrics Dashboard Concept

| Field | Value |
| ----- | ----- |
| ID | `m08-concept-quality-metrics-dashboard-concept` |
| Category | `concept` |
| Module | `module-08` |
| Lesson | 8.4 |
| Lab | lab-08 |
| Learning objective | AI strategy: Quality Metrics Dashboard Concept |
| AWS icons | Amazon CloudWatch |

## Formats

- Mermaid: [`module-08/mermaid/concept/m08-concept-quality-metrics-dashboard-concept.mmd`](module-08/mermaid/concept/m08-concept-quality-metrics-dashboard-concept.mmd)
- Draw.io: [`module-08/drawio/concept/m08-concept-quality-metrics-dashboard-concept.drawio`](module-08/drawio/concept/m08-concept-quality-metrics-dashboard-concept.drawio)
- SVG: [`module-08/svg/concept/m08-concept-quality-metrics-dashboard-concept.svg`](module-08/svg/concept/m08-concept-quality-metrics-dashboard-concept.svg)
- PNG: [`module-08/png/concept/m08-concept-quality-metrics-dashboard-concept.png`](module-08/png/concept/m08-concept-quality-metrics-dashboard-concept.png)

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
  Acc["Accuracy"] --- Lat["Latency"]
  Cost["Cost/Token"] --- Hit["HITL Rate"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
