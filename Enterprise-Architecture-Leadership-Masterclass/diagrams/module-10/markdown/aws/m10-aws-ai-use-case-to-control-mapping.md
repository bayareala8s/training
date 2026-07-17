# AI Use Case to Control Mapping

| Field | Value |
| ----- | ----- |
| ID | `m10-aws-ai-use-case-to-control-mapping` |
| Category | `aws` |
| Module | `module-10` |
| Lesson | 10.1 |
| Lab | lab-10 |
| Learning objective | Capstone visual: AI Use Case to Control Mapping |
| AWS icons | Amazon API Gateway, Amazon Bedrock, IAM |

## Formats

- Mermaid: [`module-10/mermaid/aws/m10-aws-ai-use-case-to-control-mapping.mmd`](module-10/mermaid/aws/m10-aws-ai-use-case-to-control-mapping.mmd)
- Draw.io: [`module-10/drawio/aws/m10-aws-ai-use-case-to-control-mapping.drawio`](module-10/drawio/aws/m10-aws-ai-use-case-to-control-mapping.drawio)
- SVG: [`module-10/svg/aws/m10-aws-ai-use-case-to-control-mapping.svg`](module-10/svg/aws/m10-aws-ai-use-case-to-control-mapping.svg)
- PNG: [`module-10/png/aws/m10-aws-ai-use-case-to-control-mapping.png`](module-10/png/aws/m10-aws-ai-use-case-to-control-mapping.png)

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
  UseCase --> Scorecard --> Controls --> Production
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
