# Current vs Target State Arc

| Field | Value |
| ----- | ----- |
| ID | `m01-concept-current-vs-target-state-arc` |
| Category | `concept` |
| Module | `module-01` |
| Lesson | 1.1 |
| Lab | — |
| Learning objective | Frame transformation as managed transitions |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-01/mermaid/concept/m01-concept-current-vs-target-state-arc.mmd`](module-01/mermaid/concept/m01-concept-current-vs-target-state-arc.mmd)
- Draw.io: [`module-01/drawio/concept/m01-concept-current-vs-target-state-arc.drawio`](module-01/drawio/concept/m01-concept-current-vs-target-state-arc.drawio)
- SVG: [`module-01/svg/concept/m01-concept-current-vs-target-state-arc.svg`](module-01/svg/concept/m01-concept-current-vs-target-state-arc.svg)
- PNG: [`module-01/png/concept/m01-concept-current-vs-target-state-arc.png`](module-01/png/concept/m01-concept-current-vs-target-state-arc.png)

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
  CS["Current State"] --> T1["Transition A"]
  T1 --> T2["Transition B"]
  T2 --> TS["Target State"]
  CS -.-> Risk["Risk & Debt"]
  TS -.-> Value["Business Value"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
