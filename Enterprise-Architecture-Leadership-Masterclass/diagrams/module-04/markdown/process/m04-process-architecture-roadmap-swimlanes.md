# Architecture Roadmap Swimlanes

| Field | Value |
| ----- | ----- |
| ID | `m04-process-architecture-roadmap-swimlanes` |
| Category | `process` |
| Module | `module-04` |
| Lesson | 4.4 |
| Lab | lab-04 |
| Learning objective | Design target-state: Architecture Roadmap Swimlanes |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-04/mermaid/process/m04-process-architecture-roadmap-swimlanes.mmd`](module-04/mermaid/process/m04-process-architecture-roadmap-swimlanes.mmd)
- Draw.io: [`module-04/drawio/process/m04-process-architecture-roadmap-swimlanes.drawio`](module-04/drawio/process/m04-process-architecture-roadmap-swimlanes.drawio)
- SVG: [`module-04/svg/process/m04-process-architecture-roadmap-swimlanes.svg`](module-04/svg/process/m04-process-architecture-roadmap-swimlanes.svg)
- PNG: [`module-04/png/process/m04-process-architecture-roadmap-swimlanes.png`](module-04/png/process/m04-process-architecture-roadmap-swimlanes.png)

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
  subgraph Business
    B1["Onboarding KPI"]
  end
  subgraph Platform
    P1["Landing Zone"]
    P2["Integration Hub"]
  end
  subgraph Security
    S1["Identity"]
    S2["DR"]
  end
  B1 --- P2
  P1 --> P2
  S1 --> P1
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
