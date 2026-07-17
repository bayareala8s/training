# Payment Event Flow

| Field | Value |
| ----- | ----- |
| ID | `m06-aws-payment-event-flow` |
| Category | `aws` |
| Module | `module-06` |
| Lesson | 6.3 |
| Lab | lab-06 |
| Learning objective | Integration/data architecture: Payment Event Flow |
| AWS icons | Amazon EventBridge, Amazon SQS, AWS Lambda, Amazon SNS |

## Formats

- Mermaid: [`module-06/mermaid/aws/m06-aws-payment-event-flow.mmd`](module-06/mermaid/aws/m06-aws-payment-event-flow.mmd)
- Draw.io: [`module-06/drawio/aws/m06-aws-payment-event-flow.drawio`](module-06/drawio/aws/m06-aws-payment-event-flow.drawio)
- SVG: [`module-06/svg/aws/m06-aws-payment-event-flow.svg`](module-06/svg/aws/m06-aws-payment-event-flow.svg)
- PNG: [`module-06/png/aws/m06-aws-payment-event-flow.png`](module-06/png/aws/m06-aws-payment-event-flow.png)

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
  Pay["Payment Service"] -->|event| EB["EventBridge"]
  EB --> SQS["SQS"]
  SQS --> L["Lambda"]
  L --> SNS["SNS Notification"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
