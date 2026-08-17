# Capability Ownership Model

| Field | Value |
| ----- | ----- |
| ID | `m02-concept-capability-ownership-model` |
| Category | `concept` |
| Module | `module-02` |
| Lesson | 2.2 |
| Lab | — |
| Learning objective | Apply business architecture visual: Capability Ownership Model |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-02/mermaid/concept/m02-concept-capability-ownership-model.mmd`](module-02/mermaid/concept/m02-concept-capability-ownership-model.mmd)
- Draw.io: [`module-02/drawio/concept/m02-concept-capability-ownership-model.drawio`](module-02/drawio/concept/m02-concept-capability-ownership-model.drawio)
- SVG: [`module-02/svg/concept/m02-concept-capability-ownership-model.svg`](module-02/svg/concept/m02-concept-capability-ownership-model.svg)
- PNG: [`module-02/png/concept/m02-concept-capability-ownership-model.png`](module-02/png/concept/m02-concept-capability-ownership-model.png)

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
  Cap["Capability"] --> BO["Business Owner"]
  Cap --> TO["Technical Owner"]
  Cap --> DO["Data Owner"]
  BO & TO & DO --> ADR["Joint ADRs"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
