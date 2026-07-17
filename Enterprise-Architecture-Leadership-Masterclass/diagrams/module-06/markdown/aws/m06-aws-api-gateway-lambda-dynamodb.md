# API Gateway Lambda DynamoDB

| Field | Value |
| ----- | ----- |
| ID | `m06-aws-api-gateway-lambda-dynamodb` |
| Category | `aws` |
| Module | `module-06` |
| Lesson | 6.4 |
| Lab | lab-06 |
| Learning objective | Integration/data architecture: API Gateway Lambda DynamoDB |
| AWS icons | Amazon API Gateway, AWS Lambda, Amazon DynamoDB |

## Formats

- Mermaid: [`module-06/mermaid/aws/m06-aws-api-gateway-lambda-dynamodb.mmd`](module-06/mermaid/aws/m06-aws-api-gateway-lambda-dynamodb.mmd)
- Draw.io: [`module-06/drawio/aws/m06-aws-api-gateway-lambda-dynamodb.drawio`](module-06/drawio/aws/m06-aws-api-gateway-lambda-dynamodb.drawio)
- SVG: [`module-06/svg/aws/m06-aws-api-gateway-lambda-dynamodb.svg`](module-06/svg/aws/m06-aws-api-gateway-lambda-dynamodb.svg)
- PNG: [`module-06/png/aws/m06-aws-api-gateway-lambda-dynamodb.png`](module-06/png/aws/m06-aws-api-gateway-lambda-dynamodb.png)

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
  C["Client"] --> A["API Gateway"]
  A --> L["Lambda"]
  L --> D["DynamoDB"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
