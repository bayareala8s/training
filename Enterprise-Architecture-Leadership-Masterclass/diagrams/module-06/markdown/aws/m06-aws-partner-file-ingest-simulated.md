# Partner File Ingest Simulated

| Field | Value |
| ----- | ----- |
| ID | `m06-aws-partner-file-ingest-simulated` |
| Category | `aws` |
| Module | `module-06` |
| Lesson | 6.4 |
| Lab | lab-06 |
| Learning objective | Integration/data architecture: Partner File Ingest Simulated |
| AWS icons | Amazon S3, AWS Step Functions, AWS Lambda |

## Formats

- Mermaid: [`module-06/mermaid/aws/m06-aws-partner-file-ingest-simulated.mmd`](module-06/mermaid/aws/m06-aws-partner-file-ingest-simulated.mmd)
- Draw.io: [`module-06/drawio/aws/m06-aws-partner-file-ingest-simulated.drawio`](module-06/drawio/aws/m06-aws-partner-file-ingest-simulated.drawio)
- SVG: [`module-06/svg/aws/m06-aws-partner-file-ingest-simulated.svg`](module-06/svg/aws/m06-aws-partner-file-ingest-simulated.svg)
- PNG: [`module-06/png/aws/m06-aws-partner-file-ingest-simulated.png`](module-06/png/aws/m06-aws-partner-file-ingest-simulated.png)

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
  Partner["Partner File"] --> S3["S3 Landing"]
  S3 --> SF["Step Functions"]
  SF --> Val["Validate"]
  Val --> Route["Route / Store Status"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
