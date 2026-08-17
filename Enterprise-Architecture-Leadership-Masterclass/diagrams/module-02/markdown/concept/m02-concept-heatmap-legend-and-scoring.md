# Heatmap Legend and Scoring

| Field | Value |
| ----- | ----- |
| ID | `m02-concept-heatmap-legend-and-scoring` |
| Category | `concept` |
| Module | `module-02` |
| Lesson | 2.4 |
| Lab | — |
| Learning objective | Apply business architecture visual: Heatmap Legend and Scoring |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-02/mermaid/concept/m02-concept-heatmap-legend-and-scoring.mmd`](module-02/mermaid/concept/m02-concept-heatmap-legend-and-scoring.mmd)
- Draw.io: [`module-02/drawio/concept/m02-concept-heatmap-legend-and-scoring.drawio`](module-02/drawio/concept/m02-concept-heatmap-legend-and-scoring.drawio)
- SVG: [`module-02/svg/concept/m02-concept-heatmap-legend-and-scoring.svg`](module-02/svg/concept/m02-concept-heatmap-legend-and-scoring.svg)
- PNG: [`module-02/png/concept/m02-concept-heatmap-legend-and-scoring.png`](module-02/png/concept/m02-concept-heatmap-legend-and-scoring.png)

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
  R["1–2 Red: Fragile"] --> A["3 Amber: Adequate"]
  A --> G["4–5 Green: Strong"]
  style R fill:#FCE8E6,stroke:#D13212
  style A fill:#FFF3E0,stroke:#ED7100
  style G fill:#F0F7E6,stroke:#1D8102
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
