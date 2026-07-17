# Batch Regulatory Pipeline

| Field | Value |
| ----- | ----- |
| ID | `m06-aws-batch-regulatory-pipeline` |
| Category | `aws` |
| Module | `module-06` |
| Lesson | 6.1 |
| Lab | lab-06 |
| Learning objective | Integration/data architecture: Batch Regulatory Pipeline |
| AWS icons | Amazon S3, AWS Step Functions, Amazon DynamoDB |

## Formats

- Mermaid: [`module-06/mermaid/aws/m06-aws-batch-regulatory-pipeline.mmd`](module-06/mermaid/aws/m06-aws-batch-regulatory-pipeline.mmd)
- Draw.io: [`module-06/drawio/aws/m06-aws-batch-regulatory-pipeline.drawio`](module-06/drawio/aws/m06-aws-batch-regulatory-pipeline.drawio)
- SVG: [`module-06/svg/aws/m06-aws-batch-regulatory-pipeline.svg`](module-06/svg/aws/m06-aws-batch-regulatory-pipeline.svg)
- PNG: [`module-06/png/aws/m06-aws-batch-regulatory-pipeline.png`](module-06/png/aws/m06-aws-batch-regulatory-pipeline.png)

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
  Batch["Daily Batch"] --> S3["S3"]
  S3 --> SF["Step Functions"]
  SF --> Status["DynamoDB Status"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
