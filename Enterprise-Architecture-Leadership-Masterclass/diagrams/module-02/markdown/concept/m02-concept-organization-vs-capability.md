# Organization vs Capability

| Field | Value |
| ----- | ----- |
| ID | `m02-concept-organization-vs-capability` |
| Category | `concept` |
| Module | `module-02` |
| Lesson | 2.1 |
| Lab | — |
| Learning objective | Apply business architecture visual: Organization vs Capability |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-02/mermaid/concept/m02-concept-organization-vs-capability.mmd`](module-02/mermaid/concept/m02-concept-organization-vs-capability.mmd)
- Draw.io: [`module-02/drawio/concept/m02-concept-organization-vs-capability.drawio`](module-02/drawio/concept/m02-concept-organization-vs-capability.drawio)
- SVG: [`module-02/svg/concept/m02-concept-organization-vs-capability.svg`](module-02/svg/concept/m02-concept-organization-vs-capability.svg)
- PNG: [`module-02/png/concept/m02-concept-organization-vs-capability.png`](module-02/png/concept/m02-concept-organization-vs-capability.png)

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
  Org["Org Chart<br/>(changes often)"] -.-> Cap["Capability Map<br/>(stable)"]
  Cap --> Invest["Investment Decisions"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
