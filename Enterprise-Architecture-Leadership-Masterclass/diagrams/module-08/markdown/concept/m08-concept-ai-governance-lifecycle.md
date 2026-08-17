# AI Governance Lifecycle

| Field | Value |
| ----- | ----- |
| ID | `m08-concept-ai-governance-lifecycle` |
| Category | `concept` |
| Module | `module-08` |
| Lesson | 8.4 |
| Lab | lab-08 |
| Learning objective | AI strategy: AI Governance Lifecycle |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-08/mermaid/concept/m08-concept-ai-governance-lifecycle.mmd`](module-08/mermaid/concept/m08-concept-ai-governance-lifecycle.mmd)
- Draw.io: [`module-08/drawio/concept/m08-concept-ai-governance-lifecycle.drawio`](module-08/drawio/concept/m08-concept-ai-governance-lifecycle.drawio)
- SVG: [`module-08/svg/concept/m08-concept-ai-governance-lifecycle.svg`](module-08/svg/concept/m08-concept-ai-governance-lifecycle.svg)
- PNG: [`module-08/png/concept/m08-concept-ai-governance-lifecycle.png`](module-08/png/concept/m08-concept-ai-governance-lifecycle.png)

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
  Propose["Propose Use Case"] --> Score["Scorecard"]
  Score --> Pilot["Pilot Controls"]
  Pilot --> Eval["Evaluate"]
  Eval --> Prod["Production Gate"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
