# Transfer Family Conceptual Optional

| Field | Value |
| ----- | ----- |
| ID | `m06-aws-transfer-family-conceptual-optional` |
| Category | `aws` |
| Module | `module-06` |
| Lesson | 6.1 |
| Lab | lab-06 |
| Learning objective | Integration/data architecture: Transfer Family Conceptual Optional |
| AWS icons | AWS Transfer Family, Amazon S3 |

## Formats

- Mermaid: [`module-06/mermaid/aws/m06-aws-transfer-family-conceptual-optional.mmd`](module-06/mermaid/aws/m06-aws-transfer-family-conceptual-optional.mmd)
- Draw.io: [`module-06/drawio/aws/m06-aws-transfer-family-conceptual-optional.drawio`](module-06/drawio/aws/m06-aws-transfer-family-conceptual-optional.drawio)
- SVG: [`module-06/svg/aws/m06-aws-transfer-family-conceptual-optional.svg`](module-06/svg/aws/m06-aws-transfer-family-conceptual-optional.svg)
- PNG: [`module-06/png/aws/m06-aws-transfer-family-conceptual-optional.png`](module-06/png/aws/m06-aws-transfer-family-conceptual-optional.png)

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
  Partner["SFTP Client"] --> TF["AWS Transfer Family<br/>(optional / cost)"]
  TF --> S3["S3"]
  note["Labs simulate with S3 put"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
