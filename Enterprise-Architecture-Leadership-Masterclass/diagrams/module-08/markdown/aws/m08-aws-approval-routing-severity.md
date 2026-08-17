# Approval Routing Severity

| Field | Value |
| ----- | ----- |
| ID | `m08-aws-approval-routing-severity` |
| Category | `aws` |
| Module | `module-08` |
| Lesson | 8.4 |
| Lab | lab-08 |
| Learning objective | AI strategy: Approval Routing Severity |
| AWS icons | AWS Step Functions |

## Formats

- Mermaid: [`module-08/mermaid/aws/m08-aws-approval-routing-severity.mmd`](module-08/mermaid/aws/m08-aws-approval-routing-severity.mmd)
- Draw.io: [`module-08/drawio/aws/m08-aws-approval-routing-severity.drawio`](module-08/drawio/aws/m08-aws-approval-routing-severity.drawio)
- SVG: [`module-08/svg/aws/m08-aws-approval-routing-severity.svg`](module-08/svg/aws/m08-aws-approval-routing-severity.svg)
- PNG: [`module-08/png/aws/m08-aws-approval-routing-severity.png`](module-08/png/aws/m08-aws-approval-routing-severity.png)

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
  Sev{"Severity"}
  Sev -->|Low| Auto
  Sev -->|High| HITL
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
