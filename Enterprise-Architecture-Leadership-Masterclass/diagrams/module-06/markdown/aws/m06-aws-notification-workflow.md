# Notification Workflow

| Field | Value |
| ----- | ----- |
| ID | `m06-aws-notification-workflow` |
| Category | `aws` |
| Module | `module-06` |
| Lesson | 6.2 |
| Lab | lab-06 |
| Learning objective | Integration/data architecture: Notification Workflow |
| AWS icons | Amazon SNS, Amazon EventBridge |

## Formats

- Mermaid: [`module-06/mermaid/aws/m06-aws-notification-workflow.mmd`](module-06/mermaid/aws/m06-aws-notification-workflow.mmd)
- Draw.io: [`module-06/drawio/aws/m06-aws-notification-workflow.drawio`](module-06/drawio/aws/m06-aws-notification-workflow.drawio)
- SVG: [`module-06/svg/aws/m06-aws-notification-workflow.svg`](module-06/svg/aws/m06-aws-notification-workflow.svg)
- PNG: [`module-06/png/aws/m06-aws-notification-workflow.png`](module-06/png/aws/m06-aws-notification-workflow.png)

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
  Ev["Domain Event"] --> EB["EventBridge"]
  EB --> SNS["SNS"]
  SNS --> Chan["Email / SMS / Webhook"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
