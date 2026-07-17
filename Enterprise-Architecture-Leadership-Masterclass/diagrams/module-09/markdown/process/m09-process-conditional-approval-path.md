# Conditional Approval Path

| Field | Value |
| ----- | ----- |
| ID | `m09-process-conditional-approval-path` |
| Category | `process` |
| Module | `module-09` |
| Lesson | 9.2 |
| Lab | lab-09 |
| Learning objective | Governance: Conditional Approval Path |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-09/mermaid/process/m09-process-conditional-approval-path.mmd`](module-09/mermaid/process/m09-process-conditional-approval-path.mmd)
- Draw.io: [`module-09/drawio/process/m09-process-conditional-approval-path.drawio`](module-09/drawio/process/m09-process-conditional-approval-path.drawio)
- SVG: [`module-09/svg/process/m09-process-conditional-approval-path.svg`](module-09/svg/process/m09-process-conditional-approval-path.svg)
- PNG: [`module-09/png/process/m09-process-conditional-approval-path.png`](module-09/png/process/m09-process-conditional-approval-path.png)

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
  Cond["Conditional Approve"] --> Track["Track Conditions"]
  Track --> Met{"Met?"}
  Met -->|Yes| Full["Full Approve"]
  Met -->|No| Escalate["Escalate"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
