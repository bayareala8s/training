# Portfolio Governance Cadence

| Field | Value |
| ----- | ----- |
| ID | `m09-process-portfolio-governance-cadence` |
| Category | `process` |
| Module | `module-09` |
| Lesson | 9.2 |
| Lab | lab-09 |
| Learning objective | Governance: Portfolio Governance Cadence |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-09/mermaid/process/m09-process-portfolio-governance-cadence.mmd`](module-09/mermaid/process/m09-process-portfolio-governance-cadence.mmd)
- Draw.io: [`module-09/drawio/process/m09-process-portfolio-governance-cadence.drawio`](module-09/drawio/process/m09-process-portfolio-governance-cadence.drawio)
- SVG: [`module-09/svg/process/m09-process-portfolio-governance-cadence.svg`](module-09/svg/process/m09-process-portfolio-governance-cadence.svg)
- PNG: [`module-09/png/process/m09-process-portfolio-governance-cadence.png`](module-09/png/process/m09-process-portfolio-governance-cadence.png)

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
  Weekly["Domain Reviews"] --> Monthly["ARB"]
  Monthly --> Quarterly["Portfolio Exec"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
