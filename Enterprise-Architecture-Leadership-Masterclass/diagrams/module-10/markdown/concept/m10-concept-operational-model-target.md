# Operational Model Target

| Field | Value |
| ----- | ----- |
| ID | `m10-concept-operational-model-target` |
| Category | `concept` |
| Module | `module-10` |
| Lesson | 10.4 |
| Lab | lab-10 |
| Learning objective | Capstone leadership: Operational Model Target |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-10/mermaid/concept/m10-concept-operational-model-target.mmd`](module-10/mermaid/concept/m10-concept-operational-model-target.mmd)
- Draw.io: [`module-10/drawio/concept/m10-concept-operational-model-target.drawio`](module-10/drawio/concept/m10-concept-operational-model-target.drawio)
- SVG: [`module-10/svg/concept/m10-concept-operational-model-target.svg`](module-10/svg/concept/m10-concept-operational-model-target.svg)
- PNG: [`module-10/png/concept/m10-concept-operational-model-target.png`](module-10/png/concept/m10-concept-operational-model-target.png)

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
  Prod["Product Teams"] --> GP["Golden Paths"]
  EA["EA / ARB"] --> Guard["Guardrails"]
  Guard --> Prod
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
