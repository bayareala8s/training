# Platform Before Products

| Field | Value |
| ----- | ----- |
| ID | `m04-concept-platform-before-products` |
| Category | `concept` |
| Module | `module-04` |
| Lesson | 4.2 |
| Lab | lab-04 |
| Learning objective | Design target-state: Platform Before Products |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-04/mermaid/concept/m04-concept-platform-before-products.mmd`](module-04/mermaid/concept/m04-concept-platform-before-products.mmd)
- Draw.io: [`module-04/drawio/concept/m04-concept-platform-before-products.drawio`](module-04/drawio/concept/m04-concept-platform-before-products.drawio)
- SVG: [`module-04/svg/concept/m04-concept-platform-before-products.svg`](module-04/svg/concept/m04-concept-platform-before-products.svg)
- PNG: [`module-04/png/concept/m04-concept-platform-before-products.png`](module-04/png/concept/m04-concept-platform-before-products.png)

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
  Guard["Guardrails"] --> GP["Golden Paths"]
  GP --> Prod["Product Acceleration"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
