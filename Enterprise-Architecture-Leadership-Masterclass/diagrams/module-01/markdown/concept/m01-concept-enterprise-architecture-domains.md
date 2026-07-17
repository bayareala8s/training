# Enterprise Architecture Domains

| Field | Value |
| ----- | ----- |
| ID | `m01-concept-enterprise-architecture-domains` |
| Category | `concept` |
| Module | `module-01` |
| Lesson | 1.1 |
| Lab | — |
| Learning objective | Map EA domains to NorthStar transformation scope |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-01/mermaid/concept/m01-concept-enterprise-architecture-domains.mmd`](module-01/mermaid/concept/m01-concept-enterprise-architecture-domains.mmd)
- Draw.io: [`module-01/drawio/concept/m01-concept-enterprise-architecture-domains.drawio`](module-01/drawio/concept/m01-concept-enterprise-architecture-domains.drawio)
- SVG: [`module-01/svg/concept/m01-concept-enterprise-architecture-domains.svg`](module-01/svg/concept/m01-concept-enterprise-architecture-domains.svg)
- PNG: [`module-01/png/concept/m01-concept-enterprise-architecture-domains.png`](module-01/png/concept/m01-concept-enterprise-architecture-domains.png)

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
  subgraph EA["Enterprise Architecture Domains — NorthStar (fictional)"]
    B["Business Architecture"]
    D["Data Architecture"]
    A["Application Architecture"]
    T["Technology Architecture"]
    S["Security Architecture"]
  end
  Strat["Business Strategy"] --> B
  B --> D & A
  A --> T
  B & D & A & T --> S
  S --> Outcomes["Outcomes: Cost · Speed · Risk · Visibility"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
