# Investment Priority Matrix

| Field | Value |
| ----- | ----- |
| ID | `m02-executive-investment-priority-matrix` |
| Category | `executive` |
| Module | `module-02` |
| Lesson | 2.4 |
| Lab | — |
| Learning objective | Apply business architecture visual: Investment Priority Matrix |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-02/mermaid/executive/m02-executive-investment-priority-matrix.mmd`](module-02/mermaid/executive/m02-executive-investment-priority-matrix.mmd)
- Draw.io: [`module-02/drawio/executive/m02-executive-investment-priority-matrix.drawio`](module-02/drawio/executive/m02-executive-investment-priority-matrix.drawio)
- SVG: [`module-02/svg/executive/m02-executive-investment-priority-matrix.svg`](module-02/svg/executive/m02-executive-investment-priority-matrix.svg)
- PNG: [`module-02/png/executive/m02-executive-investment-priority-matrix.png`](module-02/png/executive/m02-executive-investment-priority-matrix.png)

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
quadrantChart
    title Capability Investment Priorities
    x-axis Low Effort --> High Effort
    y-axis Low Value --> High Value
    quadrant-1 Strategic Bets
    quadrant-2 Quick Wins
    quadrant-3 Park
    quadrant-4 Foundations
    Onboarding: [0.35, 0.85]
    Integration Hub: [0.7, 0.8]
    Partner Portal: [0.55, 0.75]
    Legacy Batch: [0.8, 0.3]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
