# Token Cost Tracking

| Field | Value |
| ----- | ----- |
| ID | `m08-aws-token-cost-tracking` |
| Category | `aws` |
| Module | `module-08` |
| Lesson | 8.3 |
| Lab | lab-08 |
| Learning objective | AI strategy: Token Cost Tracking |
| AWS icons | Amazon CloudWatch, Amazon DynamoDB |

## Formats

- Mermaid: [`module-08/mermaid/aws/m08-aws-token-cost-tracking.mmd`](module-08/mermaid/aws/m08-aws-token-cost-tracking.mmd)
- Draw.io: [`module-08/drawio/aws/m08-aws-token-cost-tracking.drawio`](module-08/drawio/aws/m08-aws-token-cost-tracking.drawio)
- SVG: [`module-08/svg/aws/m08-aws-token-cost-tracking.svg`](module-08/svg/aws/m08-aws-token-cost-tracking.svg)
- PNG: [`module-08/png/aws/m08-aws-token-cost-tracking.png`](module-08/png/aws/m08-aws-token-cost-tracking.png)

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
  Call["Model Call"] --> Tokens["Token Meter"]
  Tokens --> Cost["Cost Estimate"]
  Cost --> CW["CloudWatch / Table"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
