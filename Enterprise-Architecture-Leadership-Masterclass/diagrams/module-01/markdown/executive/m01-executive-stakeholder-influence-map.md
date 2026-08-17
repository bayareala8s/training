# Stakeholder Influence Map

| Field | Value |
| ----- | ----- |
| ID | `m01-executive-stakeholder-influence-map` |
| Category | `executive` |
| Module | `module-01` |
| Lesson | 1.4 |
| Lab | — |
| Learning objective | Position stakeholders by interest and influence |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-01/mermaid/executive/m01-executive-stakeholder-influence-map.mmd`](module-01/mermaid/executive/m01-executive-stakeholder-influence-map.mmd)
- Draw.io: [`module-01/drawio/executive/m01-executive-stakeholder-influence-map.drawio`](module-01/drawio/executive/m01-executive-stakeholder-influence-map.drawio)
- SVG: [`module-01/svg/executive/m01-executive-stakeholder-influence-map.svg`](module-01/svg/executive/m01-executive-stakeholder-influence-map.svg)
- PNG: [`module-01/png/executive/m01-executive-stakeholder-influence-map.png`](module-01/png/executive/m01-executive-stakeholder-influence-map.png)

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
    title NorthStar Stakeholder Map (fictional)
    x-axis Low Influence --> High Influence
    y-axis Low Interest --> High Interest
    quadrant-1 Manage Closely
    quadrant-2 Keep Informed
    quadrant-3 Monitor
    quadrant-4 Keep Satisfied
    CEO: [0.8, 0.85]
    CIO: [0.75, 0.9]
    CISO: [0.7, 0.8]
    BU President: [0.65, 0.7]
    Platform Lead: [0.55, 0.75]
    Eng Managers: [0.45, 0.6]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
