# EventBridge Fan-out

| Field | Value |
| ----- | ----- |
| ID | `m06-aws-eventbridge-fan-out` |
| Category | `aws` |
| Module | `module-06` |
| Lesson | 6.4 |
| Lab | lab-06 |
| Learning objective | Integration/data architecture: EventBridge Fan-out |
| AWS icons | Amazon EventBridge, AWS Lambda |

## Formats

- Mermaid: [`module-06/mermaid/aws/m06-aws-eventbridge-fan-out.mmd`](module-06/mermaid/aws/m06-aws-eventbridge-fan-out.mmd)
- Draw.io: [`module-06/drawio/aws/m06-aws-eventbridge-fan-out.drawio`](module-06/drawio/aws/m06-aws-eventbridge-fan-out.drawio)
- SVG: [`module-06/svg/aws/m06-aws-eventbridge-fan-out.svg`](module-06/svg/aws/m06-aws-eventbridge-fan-out.svg)
- PNG: [`module-06/png/aws/m06-aws-eventbridge-fan-out.png`](module-06/png/aws/m06-aws-eventbridge-fan-out.png)

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
  Prod["Producer"] --> EB["EventBridge"]
  EB --> R1["Rule → Fraud"]
  EB --> R2["Rule → Analytics"]
  EB --> R3["Rule → Notify"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
