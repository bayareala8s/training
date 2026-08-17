# Influence Without Authority Loop

| Field | Value |
| ----- | ----- |
| ID | `m01-process-influence-without-authority-loop` |
| Category | `process` |
| Module | `module-01` |
| Lesson | 1.4 |
| Lab | — |
| Learning objective | Show how EAs create alignment without hierarchy |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-01/mermaid/process/m01-process-influence-without-authority-loop.mmd`](module-01/mermaid/process/m01-process-influence-without-authority-loop.mmd)
- Draw.io: [`module-01/drawio/process/m01-process-influence-without-authority-loop.drawio`](module-01/drawio/process/m01-process-influence-without-authority-loop.drawio)
- SVG: [`module-01/svg/process/m01-process-influence-without-authority-loop.svg`](module-01/svg/process/m01-process-influence-without-authority-loop.svg)
- PNG: [`module-01/png/process/m01-process-influence-without-authority-loop.png`](module-01/png/process/m01-process-influence-without-authority-loop.png)

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
  Listen["Listen & Diagnose"] --> Frame["Frame Trade-offs"]
  Frame --> Coal["Build Coalition"]
  Coal --> Dec["Decide via ADR/ARB"]
  Dec --> Prove["Prove with Outcomes"]
  Prove --> Listen
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
