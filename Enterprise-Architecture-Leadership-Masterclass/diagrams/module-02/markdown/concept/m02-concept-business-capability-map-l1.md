# Business Capability Map L1

| Field | Value |
| ----- | ----- |
| ID | `m02-concept-business-capability-map-l1` |
| Category | `concept` |
| Module | `module-02` |
| Lesson | 2.1 |
| Lab | — |
| Learning objective | Apply business architecture visual: Business Capability Map L1 |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-02/mermaid/concept/m02-concept-business-capability-map-l1.mmd`](module-02/mermaid/concept/m02-concept-business-capability-map-l1.mmd)
- Draw.io: [`module-02/drawio/concept/m02-concept-business-capability-map-l1.drawio`](module-02/drawio/concept/m02-concept-business-capability-map-l1.drawio)
- SVG: [`module-02/svg/concept/m02-concept-business-capability-map-l1.svg`](module-02/svg/concept/m02-concept-business-capability-map-l1.svg)
- PNG: [`module-02/png/concept/m02-concept-business-capability-map-l1.png`](module-02/png/concept/m02-concept-business-capability-map-l1.png)

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
  subgraph NorthStar["NorthStar L1 Capabilities (fictional)"]
    C1["Customer Management"]
    C2["Payments"]
    C3["Partner Management"]
    C4["Risk & Compliance"]
    C5["Product Management"]
    C6["Data & Analytics"]
    C7["Enterprise Platforms"]
    C8["Workforce"]
  end
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
