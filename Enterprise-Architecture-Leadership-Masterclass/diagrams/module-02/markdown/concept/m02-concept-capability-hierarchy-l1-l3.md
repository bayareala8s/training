# Capability Hierarchy L1-L3

| Field | Value |
| ----- | ----- |
| ID | `m02-concept-capability-hierarchy-l1-l3` |
| Category | `concept` |
| Module | `module-02` |
| Lesson | 2.2 |
| Lab | — |
| Learning objective | Apply business architecture visual: Capability Hierarchy L1-L3 |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-02/mermaid/concept/m02-concept-capability-hierarchy-l1-l3.mmd`](module-02/mermaid/concept/m02-concept-capability-hierarchy-l1-l3.mmd)
- Draw.io: [`module-02/drawio/concept/m02-concept-capability-hierarchy-l1-l3.drawio`](module-02/drawio/concept/m02-concept-capability-hierarchy-l1-l3.drawio)
- SVG: [`module-02/svg/concept/m02-concept-capability-hierarchy-l1-l3.svg`](module-02/svg/concept/m02-concept-capability-hierarchy-l1-l3.svg)
- PNG: [`module-02/png/concept/m02-concept-capability-hierarchy-l1-l3.png`](module-02/png/concept/m02-concept-capability-hierarchy-l1-l3.png)

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
  L1["L1 Customer Management"] --> L2a["L2 Onboarding"]
  L1 --> L2b["L2 Servicing"]
  L2a --> L3a["L3 KYC"]
  L2a --> L3b["L3 Account Opening"]
  L2a --> L3c["L3 Identity Proofing"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
