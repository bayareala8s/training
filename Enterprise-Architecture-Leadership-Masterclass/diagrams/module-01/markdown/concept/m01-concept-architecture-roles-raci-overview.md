# Architecture Roles RACI Overview

| Field | Value |
| ----- | ----- |
| ID | `m01-concept-architecture-roles-raci-overview` |
| Category | `concept` |
| Module | `module-01` |
| Lesson | 1.2 |
| Lab | — |
| Learning objective | Show role boundaries across EA, domain, solution, platform |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-01/mermaid/concept/m01-concept-architecture-roles-raci-overview.mmd`](module-01/mermaid/concept/m01-concept-architecture-roles-raci-overview.mmd)
- Draw.io: [`module-01/drawio/concept/m01-concept-architecture-roles-raci-overview.drawio`](module-01/drawio/concept/m01-concept-architecture-roles-raci-overview.drawio)
- SVG: [`module-01/svg/concept/m01-concept-architecture-roles-raci-overview.svg`](module-01/svg/concept/m01-concept-architecture-roles-raci-overview.svg)
- PNG: [`module-01/png/concept/m01-concept-architecture-roles-raci-overview.png`](module-01/png/concept/m01-concept-architecture-roles-raci-overview.png)

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
  CIO["CIO / CTO"] --> EA["Lead Enterprise Architect"]
  EA --> DA["Domain Architects"]
  EA --> PA["Platform Architects"]
  DA --> SA["Solution Architects"]
  PA --> SA
  EA --> ARB["Architecture Review Board"]
  ARB --> Dec["Decisions / Exceptions"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
