# TIME Decision Tree

| Field | Value |
| ----- | ----- |
| ID | `m03-process-time-decision-tree` |
| Category | `process` |
| Module | `module-03` |
| Lesson | 3.3 |
| Lab | lab-03 |
| Learning objective | Assess current estate: TIME Decision Tree |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-03/mermaid/process/m03-process-time-decision-tree.mmd`](module-03/mermaid/process/m03-process-time-decision-tree.mmd)
- Draw.io: [`module-03/drawio/process/m03-process-time-decision-tree.drawio`](module-03/drawio/process/m03-process-time-decision-tree.drawio)
- SVG: [`module-03/svg/process/m03-process-time-decision-tree.svg`](module-03/svg/process/m03-process-time-decision-tree.svg)
- PNG: [`module-03/png/process/m03-process-time-decision-tree.png`](module-03/png/process/m03-process-time-decision-tree.png)

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
  Start["App Assessment"] --> Q1{Strategic Fit High?}
  Q1 -->|Yes| Q2{Health Strong?}
  Q1 -->|No| Q3{Still Required?}
  Q2 -->|Yes| Invest["Invest"]
  Q2 -->|No| Migrate["Migrate / Modernize"]
  Q3 -->|Yes| Tolerate["Tolerate (timebox)"]
  Q3 -->|No| Eliminate["Eliminate"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
