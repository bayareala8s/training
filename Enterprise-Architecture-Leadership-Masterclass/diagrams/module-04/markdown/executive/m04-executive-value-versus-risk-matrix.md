# Value versus Risk Matrix

| Field | Value |
| ----- | ----- |
| ID | `m04-executive-value-versus-risk-matrix` |
| Category | `executive` |
| Module | `module-04` |
| Lesson | 4.2 |
| Lab | lab-04 |
| Learning objective | Design target-state: Value versus Risk Matrix |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-04/mermaid/executive/m04-executive-value-versus-risk-matrix.mmd`](module-04/mermaid/executive/m04-executive-value-versus-risk-matrix.mmd)
- Draw.io: [`module-04/drawio/executive/m04-executive-value-versus-risk-matrix.drawio`](module-04/drawio/executive/m04-executive-value-versus-risk-matrix.drawio)
- SVG: [`module-04/svg/executive/m04-executive-value-versus-risk-matrix.svg`](module-04/svg/executive/m04-executive-value-versus-risk-matrix.svg)
- PNG: [`module-04/png/executive/m04-executive-value-versus-risk-matrix.png`](module-04/png/executive/m04-executive-value-versus-risk-matrix.png)

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
    title Value vs Risk Reduction
    x-axis Low Risk Reduction --> High Risk Reduction
    y-axis Low Value --> High Value
    quadrant-1 Do First
    quadrant-2 Value Plays
    quadrant-3 Later
    quadrant-4 Risk Must-Dos
    Integration Hub: [0.75, 0.85]
    DR Uplift: [0.9, 0.7]
    AI Assistant: [0.4, 0.65]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
