# Three Transition States

| Field | Value |
| ----- | ----- |
| ID | `m04-concept-three-transition-states` |
| Category | `concept` |
| Module | `module-04` |
| Lesson | 4.4 |
| Lab | lab-04 |
| Learning objective | Design target-state: Three Transition States |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-04/mermaid/concept/m04-concept-three-transition-states.mmd`](module-04/mermaid/concept/m04-concept-three-transition-states.mmd)
- Draw.io: [`module-04/drawio/concept/m04-concept-three-transition-states.drawio`](module-04/drawio/concept/m04-concept-three-transition-states.drawio)
- SVG: [`module-04/svg/concept/m04-concept-three-transition-states.svg`](module-04/svg/concept/m04-concept-three-transition-states.svg)
- PNG: [`module-04/png/concept/m04-concept-three-transition-states.png`](module-04/png/concept/m04-concept-three-transition-states.png)

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
  CS["Current"] --> TA["Transition A<br/>Guardrails + Hub"]
  TA --> TB["Transition B<br/>Platform Scale"]
  TB --> TS["Target<br/>Standardized"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
