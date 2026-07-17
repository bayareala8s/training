# KPI to Capability Traceability

| Field | Value |
| ----- | ----- |
| ID | `m02-process-kpi-to-capability-traceability` |
| Category | `process` |
| Module | `module-02` |
| Lesson | 2.2 |
| Lab | — |
| Learning objective | Apply business architecture visual: KPI to Capability Traceability |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-02/mermaid/process/m02-process-kpi-to-capability-traceability.mmd`](module-02/mermaid/process/m02-process-kpi-to-capability-traceability.mmd)
- Draw.io: [`module-02/drawio/process/m02-process-kpi-to-capability-traceability.drawio`](module-02/drawio/process/m02-process-kpi-to-capability-traceability.drawio)
- SVG: [`module-02/svg/process/m02-process-kpi-to-capability-traceability.svg`](module-02/svg/process/m02-process-kpi-to-capability-traceability.svg)
- PNG: [`module-02/png/process/m02-process-kpi-to-capability-traceability.png`](module-02/png/process/m02-process-kpi-to-capability-traceability.png)

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
  KPI["KPI: Onboarding Cycle Time"] --> Cap["Capability: Customer Onboarding"]
  Cap --> Arch["Architecture Levers"]
  Arch --> Init["Roadmap Initiatives"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
