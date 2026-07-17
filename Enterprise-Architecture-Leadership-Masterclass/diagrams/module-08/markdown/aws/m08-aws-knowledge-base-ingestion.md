# Knowledge Base Ingestion

| Field | Value |
| ----- | ----- |
| ID | `m08-aws-knowledge-base-ingestion` |
| Category | `aws` |
| Module | `module-08` |
| Lesson | 8.3 |
| Lab | lab-08 |
| Learning objective | AI strategy: Knowledge Base Ingestion |
| AWS icons | Amazon S3, Amazon Bedrock |

## Formats

- Mermaid: [`module-08/mermaid/aws/m08-aws-knowledge-base-ingestion.mmd`](module-08/mermaid/aws/m08-aws-knowledge-base-ingestion.mmd)
- Draw.io: [`module-08/drawio/aws/m08-aws-knowledge-base-ingestion.drawio`](module-08/drawio/aws/m08-aws-knowledge-base-ingestion.drawio)
- SVG: [`module-08/svg/aws/m08-aws-knowledge-base-ingestion.svg`](module-08/svg/aws/m08-aws-knowledge-base-ingestion.svg)
- PNG: [`module-08/png/aws/m08-aws-knowledge-base-ingestion.png`](module-08/png/aws/m08-aws-knowledge-base-ingestion.png)

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
  Docs["Approved Docs"] --> S3["S3"]
  S3 --> Ingest["Ingest / Index"]
  Ingest --> KB["Knowledge Base"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
