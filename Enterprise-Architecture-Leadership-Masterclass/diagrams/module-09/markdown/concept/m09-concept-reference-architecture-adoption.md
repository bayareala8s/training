# Reference Architecture Adoption

| Field | Value |
| ----- | ----- |
| ID | `m09-concept-reference-architecture-adoption` |
| Category | `concept` |
| Module | `module-09` |
| Lesson | 9.1 |
| Lab | lab-09 |
| Learning objective | Governance: Reference Architecture Adoption |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-09/mermaid/concept/m09-concept-reference-architecture-adoption.mmd`](module-09/mermaid/concept/m09-concept-reference-architecture-adoption.mmd)
- Draw.io: [`module-09/drawio/concept/m09-concept-reference-architecture-adoption.drawio`](module-09/drawio/concept/m09-concept-reference-architecture-adoption.drawio)
- SVG: [`module-09/svg/concept/m09-concept-reference-architecture-adoption.svg`](module-09/svg/concept/m09-concept-reference-architecture-adoption.svg)
- PNG: [`module-09/png/concept/m09-concept-reference-architecture-adoption.png`](module-09/png/concept/m09-concept-reference-architecture-adoption.png)

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
  RA["Reference Architecture"] --> Adopt["Adopt"]
  RA --> Adapt["Adapt with ADR"]
  RA --> Exception["Exception"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
