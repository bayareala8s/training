# Data Product Ownership

| Field | Value |
| ----- | ----- |
| ID | `m06-concept-data-product-ownership` |
| Category | `concept` |
| Module | `module-06` |
| Lesson | 6.4 |
| Lab | lab-06 |
| Learning objective | Integration/data architecture: Data Product Ownership |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-06/mermaid/concept/m06-concept-data-product-ownership.mmd`](module-06/mermaid/concept/m06-concept-data-product-ownership.mmd)
- Draw.io: [`module-06/drawio/concept/m06-concept-data-product-ownership.drawio`](module-06/drawio/concept/m06-concept-data-product-ownership.drawio)
- SVG: [`module-06/svg/concept/m06-concept-data-product-ownership.svg`](module-06/svg/concept/m06-concept-data-product-ownership.svg)
- PNG: [`module-06/png/concept/m06-concept-data-product-ownership.png`](module-06/png/concept/m06-concept-data-product-ownership.png)

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
  Dom["Domain Team"] --> DP["Data Product"]
  DP --> Contr["Contracts / Quality"]
  DP --> Cons["Consumers"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
