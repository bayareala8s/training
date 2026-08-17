# AI Operating Model

| Field | Value |
| ----- | ----- |
| ID | `m08-concept-ai-operating-model` |
| Category | `concept` |
| Module | `module-08` |
| Lesson | 8.2 |
| Lab | lab-08 |
| Learning objective | AI strategy: AI Operating Model |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-08/mermaid/concept/m08-concept-ai-operating-model.mmd`](module-08/mermaid/concept/m08-concept-ai-operating-model.mmd)
- Draw.io: [`module-08/drawio/concept/m08-concept-ai-operating-model.drawio`](module-08/drawio/concept/m08-concept-ai-operating-model.drawio)
- SVG: [`module-08/svg/concept/m08-concept-ai-operating-model.svg`](module-08/svg/concept/m08-concept-ai-operating-model.svg)
- PNG: [`module-08/png/concept/m08-concept-ai-operating-model.png`](module-08/png/concept/m08-concept-ai-operating-model.png)

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
  Biz["Business Sponsor"] --> Plat["AI Platform Team"]
  Plat --> Dom["Domain Teams"]
  Plat --> Risk["Risk / Compliance"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
