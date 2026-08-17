# Architecture Governance Flow

| Field | Value |
| ----- | ----- |
| ID | `m01-process-architecture-governance-flow` |
| Category | `process` |
| Module | `module-01` |
| Lesson | 1.2 |
| Lab | — |
| Learning objective | Describe how proposals move from intake to decision |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-01/mermaid/process/m01-process-architecture-governance-flow.mmd`](module-01/mermaid/process/m01-process-architecture-governance-flow.mmd)
- Draw.io: [`module-01/drawio/process/m01-process-architecture-governance-flow.drawio`](module-01/drawio/process/m01-process-architecture-governance-flow.drawio)
- SVG: [`module-01/svg/process/m01-process-architecture-governance-flow.svg`](module-01/svg/process/m01-process-architecture-governance-flow.svg)
- PNG: [`module-01/png/process/m01-process-architecture-governance-flow.png`](module-01/png/process/m01-process-architecture-governance-flow.png)

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
  Intake["1 Intake"] --> Align["2 Principle Alignment"]
  Align --> Review["3 ARB / Design Authority"]
  Review --> Dec{"Decision"}
  Dec -->|Approve| Impl["Implement + ADR"]
  Dec -->|Conditional| Cond["Conditions + Re-review"]
  Dec -->|Reject| Alt["Alternatives"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
