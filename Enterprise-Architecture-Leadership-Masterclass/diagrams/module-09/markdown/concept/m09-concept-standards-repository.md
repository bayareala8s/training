# Standards Repository

| Field | Value |
| ----- | ----- |
| ID | `m09-concept-standards-repository` |
| Category | `concept` |
| Module | `module-09` |
| Lesson | 9.1 |
| Lab | lab-09 |
| Learning objective | Governance: Standards Repository |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-09/mermaid/concept/m09-concept-standards-repository.mmd`](module-09/mermaid/concept/m09-concept-standards-repository.mmd)
- Draw.io: [`module-09/drawio/concept/m09-concept-standards-repository.drawio`](module-09/drawio/concept/m09-concept-standards-repository.drawio)
- SVG: [`module-09/svg/concept/m09-concept-standards-repository.svg`](module-09/svg/concept/m09-concept-standards-repository.svg)
- PNG: [`module-09/png/concept/m09-concept-standards-repository.png`](module-09/png/concept/m09-concept-standards-repository.png)

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
  Ref["Reference Architectures"] --> Std["Standards"]
  Std --> Patterns["Patterns"]
  Patterns --> Teams["Delivery Teams"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
