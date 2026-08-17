# AI Gateway Pattern

| Field | Value |
| ----- | ----- |
| ID | `m08-aws-ai-gateway-pattern` |
| Category | `aws` |
| Module | `module-08` |
| Lesson | 8.3 |
| Lab | lab-08 |
| Learning objective | AI strategy: AI Gateway Pattern |
| AWS icons | Amazon API Gateway, Amazon Bedrock |

## Formats

- Mermaid: [`module-08/mermaid/aws/m08-aws-ai-gateway-pattern.mmd`](module-08/mermaid/aws/m08-aws-ai-gateway-pattern.mmd)
- Draw.io: [`module-08/drawio/aws/m08-aws-ai-gateway-pattern.drawio`](module-08/drawio/aws/m08-aws-ai-gateway-pattern.drawio)
- SVG: [`module-08/svg/aws/m08-aws-ai-gateway-pattern.svg`](module-08/svg/aws/m08-aws-ai-gateway-pattern.svg)
- PNG: [`module-08/png/aws/m08-aws-ai-gateway-pattern.png`](module-08/png/aws/m08-aws-ai-gateway-pattern.png)

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
  Cons["Consumers"] --> GW["Model Gateway"]
  GW --> Auth["AuthZ"]
  GW --> Bedrock["Bedrock Models"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
