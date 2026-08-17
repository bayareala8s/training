# Coexistence Pattern

| Field | Value |
| ----- | ----- |
| ID | `m04-infrastructure-coexistence-pattern` |
| Category | `infrastructure` |
| Module | `module-04` |
| Lesson | 4.3 |
| Lab | lab-04 |
| Learning objective | Design target-state: Coexistence Pattern |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-04/mermaid/infrastructure/m04-infrastructure-coexistence-pattern.mmd`](module-04/mermaid/infrastructure/m04-infrastructure-coexistence-pattern.mmd)
- Draw.io: [`module-04/drawio/infrastructure/m04-infrastructure-coexistence-pattern.drawio`](module-04/drawio/infrastructure/m04-infrastructure-coexistence-pattern.drawio)
- SVG: [`module-04/svg/infrastructure/m04-infrastructure-coexistence-pattern.svg`](module-04/svg/infrastructure/m04-infrastructure-coexistence-pattern.svg)
- PNG: [`module-04/png/infrastructure/m04-infrastructure-coexistence-pattern.png`](module-04/png/infrastructure/m04-infrastructure-coexistence-pattern.png)

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
  Legacy["Legacy Core"] <-->|Sync / Anti-corruption| Hub["Integration Hub"]
  Hub <--> Modern["Modern Services"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
