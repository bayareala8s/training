# Hybrid Cloud Placement

| Field | Value |
| ----- | ----- |
| ID | `m05-concept-hybrid-cloud-placement` |
| Category | `concept` |
| Module | `module-05` |
| Lesson | 5.3 |
| Lab | lab-05 |
| Learning objective | Cloud/platform strategy: Hybrid Cloud Placement |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-05/mermaid/concept/m05-concept-hybrid-cloud-placement.mmd`](module-05/mermaid/concept/m05-concept-hybrid-cloud-placement.mmd)
- Draw.io: [`module-05/drawio/concept/m05-concept-hybrid-cloud-placement.drawio`](module-05/drawio/concept/m05-concept-hybrid-cloud-placement.drawio)
- SVG: [`module-05/svg/concept/m05-concept-hybrid-cloud-placement.svg`](module-05/svg/concept/m05-concept-hybrid-cloud-placement.svg)
- PNG: [`module-05/png/concept/m05-concept-hybrid-cloud-placement.png`](module-05/png/concept/m05-concept-hybrid-cloud-placement.png)

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
  OnPrem["On-Prem (retain)"] --> Criteria["Placement Criteria"]
  Criteria --> AWS["AWS (default modern)"]
  Criteria --> SaaS["SaaS (buy)"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
