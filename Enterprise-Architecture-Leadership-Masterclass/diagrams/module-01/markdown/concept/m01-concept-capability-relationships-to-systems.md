# Capability Relationships to Systems

| Field | Value |
| ----- | ----- |
| ID | `m01-concept-capability-relationships-to-systems` |
| Category | `concept` |
| Module | `module-01` |
| Lesson | 1.1 |
| Lab | — |
| Learning objective | Show capabilities independent of systems |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-01/mermaid/concept/m01-concept-capability-relationships-to-systems.mmd`](module-01/mermaid/concept/m01-concept-capability-relationships-to-systems.mmd)
- Draw.io: [`module-01/drawio/concept/m01-concept-capability-relationships-to-systems.drawio`](module-01/drawio/concept/m01-concept-capability-relationships-to-systems.drawio)
- SVG: [`module-01/svg/concept/m01-concept-capability-relationships-to-systems.svg`](module-01/svg/concept/m01-concept-capability-relationships-to-systems.svg)
- PNG: [`module-01/png/concept/m01-concept-capability-relationships-to-systems.png`](module-01/png/concept/m01-concept-capability-relationships-to-systems.png)

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
  Cap["Capability:<br/>Customer Onboarding"] --> P["Process"]
  Cap --> Data["Data Objects"]
  Cap --> Sys["Systems / Apps"]
  Cap --> Own["Business Owner"]
  note["Systems change; capability persists"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
