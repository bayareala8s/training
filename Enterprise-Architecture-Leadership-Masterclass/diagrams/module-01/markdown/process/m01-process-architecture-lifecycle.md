# Architecture Lifecycle

| Field | Value |
| ----- | ----- |
| ID | `m01-process-architecture-lifecycle` |
| Category | `process` |
| Module | `module-01` |
| Lesson | 1.1 |
| Lab | — |
| Learning objective | Show continuous architecture cycle |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-01/mermaid/process/m01-process-architecture-lifecycle.mmd`](module-01/mermaid/process/m01-process-architecture-lifecycle.mmd)
- Draw.io: [`module-01/drawio/process/m01-process-architecture-lifecycle.drawio`](module-01/drawio/process/m01-process-architecture-lifecycle.drawio)
- SVG: [`module-01/svg/process/m01-process-architecture-lifecycle.svg`](module-01/svg/process/m01-process-architecture-lifecycle.svg)
- PNG: [`module-01/png/process/m01-process-architecture-lifecycle.png`](module-01/png/process/m01-process-architecture-lifecycle.png)

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
  Disc["Discover"] --> Assess["Assess"]
  Assess --> Target["Target"]
  Target --> Road["Roadmap"]
  Road --> Gov["Govern"]
  Gov --> Disc
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
