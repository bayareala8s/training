# Business Outcome Tree

| Field | Value |
| ----- | ----- |
| ID | `m02-executive-business-outcome-tree` |
| Category | `executive` |
| Module | `module-02` |
| Lesson | 2.2 |
| Lab | — |
| Learning objective | Apply business architecture visual: Business Outcome Tree |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-02/mermaid/executive/m02-executive-business-outcome-tree.mmd`](module-02/mermaid/executive/m02-executive-business-outcome-tree.mmd)
- Draw.io: [`module-02/drawio/executive/m02-executive-business-outcome-tree.drawio`](module-02/drawio/executive/m02-executive-business-outcome-tree.drawio)
- SVG: [`module-02/svg/executive/m02-executive-business-outcome-tree.svg`](module-02/svg/executive/m02-executive-business-outcome-tree.svg)
- PNG: [`module-02/png/executive/m02-executive-business-outcome-tree.png`](module-02/png/executive/m02-executive-business-outcome-tree.png)

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
  Goal["Reduce OpEx 20% + Faster Products"] --> O1["Consolidate Platforms"]
  Goal --> O2["Improve Onboarding"]
  Goal --> O3["Governed AI"]
  O1 --> C1["Integration · Cloud"]
  O2 --> C2["Customer · Data"]
  O3 --> C3["AI Platform"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
