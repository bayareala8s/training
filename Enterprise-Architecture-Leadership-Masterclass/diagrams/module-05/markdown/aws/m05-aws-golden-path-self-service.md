# Golden Path Self-Service

| Field | Value |
| ----- | ----- |
| ID | `m05-aws-golden-path-self-service` |
| Category | `aws` |
| Module | `module-05` |
| Lesson | 5.2 |
| Lab | lab-05 |
| Learning objective | Cloud/platform strategy: Golden Path Self-Service |
| AWS icons | Amazon API Gateway, AWS Lambda, Amazon DynamoDB, AWS Systems Manager |

## Formats

- Mermaid: [`module-05/mermaid/aws/m05-aws-golden-path-self-service.mmd`](module-05/mermaid/aws/m05-aws-golden-path-self-service.mmd)
- Draw.io: [`module-05/drawio/aws/m05-aws-golden-path-self-service.drawio`](module-05/drawio/aws/m05-aws-golden-path-self-service.drawio)
- SVG: [`module-05/svg/aws/m05-aws-golden-path-self-service.svg`](module-05/svg/aws/m05-aws-golden-path-self-service.svg)
- PNG: [`module-05/png/aws/m05-aws-golden-path-self-service.png`](module-05/png/aws/m05-aws-golden-path-self-service.png)

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
  Dev["Developer"] --> APIGW["API Gateway"]
  APIGW --> L["Lambda"]
  L --> DDB["DynamoDB"]
  L --> SSM["Parameter Store"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
