# Decision Memo Structure

| Field | Value |
| ----- | ----- |
| ID | `m09-executive-decision-memo-structure` |
| Category | `executive` |
| Module | `module-09` |
| Lesson | 9.1 |
| Lab | lab-09 |
| Learning objective | Governance: Decision Memo Structure |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-09/mermaid/executive/m09-executive-decision-memo-structure.mmd`](module-09/mermaid/executive/m09-executive-decision-memo-structure.mmd)
- Draw.io: [`module-09/drawio/executive/m09-executive-decision-memo-structure.drawio`](module-09/drawio/executive/m09-executive-decision-memo-structure.drawio)
- SVG: [`module-09/svg/executive/m09-executive-decision-memo-structure.svg`](module-09/svg/executive/m09-executive-decision-memo-structure.svg)
- PNG: [`module-09/png/executive/m09-executive-decision-memo-structure.png`](module-09/png/executive/m09-executive-decision-memo-structure.png)

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
  Rec["Recommendation"] --> Why["Why Now"]
  Why --> Options["Options"]
  Options --> Ask["Clear Ask"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
