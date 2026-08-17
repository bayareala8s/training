# Business Value vs Tech Health

| Field | Value |
| ----- | ----- |
| ID | `m03-executive-business-value-vs-tech-health` |
| Category | `executive` |
| Module | `module-03` |
| Lesson | 3.1 |
| Lab | lab-03 |
| Learning objective | Assess current estate: Business Value vs Tech Health |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-03/mermaid/executive/m03-executive-business-value-vs-tech-health.mmd`](module-03/mermaid/executive/m03-executive-business-value-vs-tech-health.mmd)
- Draw.io: [`module-03/drawio/executive/m03-executive-business-value-vs-tech-health.drawio`](module-03/drawio/executive/m03-executive-business-value-vs-tech-health.drawio)
- SVG: [`module-03/svg/executive/m03-executive-business-value-vs-tech-health.svg`](module-03/svg/executive/m03-executive-business-value-vs-tech-health.svg)
- PNG: [`module-03/png/executive/m03-executive-business-value-vs-tech-health.png`](module-03/png/executive/m03-executive-business-value-vs-tech-health.png)

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
    title Portfolio Value vs Health
    x-axis Poor Health --> Strong Health
    y-axis Low Value --> High Value
    quadrant-1 Invest
    quadrant-2 Migrate
    quadrant-3 Eliminate
    quadrant-4 Tolerate
    PulsePay: [0.7, 0.9]
    Mainstreet: [0.2, 0.8]
    SFTP East: [0.35, 0.4]
    Loyalty: [0.55, 0.25]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
