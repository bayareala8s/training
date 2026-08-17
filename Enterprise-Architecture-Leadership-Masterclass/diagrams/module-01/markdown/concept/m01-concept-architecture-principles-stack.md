# Architecture Principles Stack

| Field | Value |
| ----- | ----- |
| ID | `m01-concept-architecture-principles-stack` |
| Category | `concept` |
| Module | `module-01` |
| Lesson | 1.3 |
| Lab | — |
| Learning objective | Relate principles to exceptions and metrics |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-01/mermaid/concept/m01-concept-architecture-principles-stack.mmd`](module-01/mermaid/concept/m01-concept-architecture-principles-stack.mmd)
- Draw.io: [`module-01/drawio/concept/m01-concept-architecture-principles-stack.drawio`](module-01/drawio/concept/m01-concept-architecture-principles-stack.drawio)
- SVG: [`module-01/svg/concept/m01-concept-architecture-principles-stack.svg`](module-01/svg/concept/m01-concept-architecture-principles-stack.svg)
- PNG: [`module-01/png/concept/m01-concept-architecture-principles-stack.png`](module-01/png/concept/m01-concept-architecture-principles-stack.png)

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
  Mission["Architecture Mission"] --> Prin["Principles 8–10"]
  Prin --> Impl["Implications for Teams"]
  Prin --> Exc["Exception Process"]
  Prin --> Met["Signals / Metrics"]
  Exc --> ARB["ARB Decision"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
