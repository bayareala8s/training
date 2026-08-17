# Technology Layer View

| Field | Value |
| ----- | ----- |
| ID | `cap-infrastructure-technology-layer-view` |
| Category | `infrastructure` |
| Module | `cap` |
| Lesson | — |
| Lab | lab-10 |
| Learning objective | Capstone integrated view: Technology Layer View |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`capstone/mermaid/infrastructure/cap-infrastructure-technology-layer-view.mmd`](capstone/mermaid/infrastructure/cap-infrastructure-technology-layer-view.mmd)
- Draw.io: [`capstone/drawio/infrastructure/cap-infrastructure-technology-layer-view.drawio`](capstone/drawio/infrastructure/cap-infrastructure-technology-layer-view.drawio)
- SVG: [`capstone/svg/infrastructure/cap-infrastructure-technology-layer-view.svg`](capstone/svg/infrastructure/cap-infrastructure-technology-layer-view.svg)
- PNG: [`capstone/png/infrastructure/cap-infrastructure-technology-layer-view.png`](capstone/png/infrastructure/cap-infrastructure-technology-layer-view.png)

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
  LZ["Landing Zone"] --> Comp["Compute Patterns"]
  LZ --> Data["Data Platform"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
