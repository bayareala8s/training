# Guardrails Overlay

| Field | Value |
| ----- | ----- |
| ID | `m08-aws-guardrails-overlay` |
| Category | `aws` |
| Module | `module-08` |
| Lesson | 8.2 |
| Lab | lab-08 |
| Learning objective | AI strategy: Guardrails Overlay |
| AWS icons | Amazon Bedrock |

## Formats

- Mermaid: [`module-08/mermaid/aws/m08-aws-guardrails-overlay.mmd`](module-08/mermaid/aws/m08-aws-guardrails-overlay.mmd)
- Draw.io: [`module-08/drawio/aws/m08-aws-guardrails-overlay.drawio`](module-08/drawio/aws/m08-aws-guardrails-overlay.drawio)
- SVG: [`module-08/svg/aws/m08-aws-guardrails-overlay.svg`](module-08/svg/aws/m08-aws-guardrails-overlay.svg)
- PNG: [`module-08/png/aws/m08-aws-guardrails-overlay.png`](module-08/png/aws/m08-aws-guardrails-overlay.png)

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
  Input --> GuardIn["Input Guardrails"]
  GuardIn --> Model["Model"]
  Model --> GuardOut["Output Guardrails"]
  GuardOut --> App
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
