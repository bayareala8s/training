# RAG Conceptual

| Field | Value |
| ----- | ----- |
| ID | `m08-aws-rag-conceptual` |
| Category | `aws` |
| Module | `module-08` |
| Lesson | 8.4 |
| Lab | lab-08 |
| Learning objective | AI strategy: RAG Conceptual |
| AWS icons | Amazon Bedrock, Amazon S3 |

## Formats

- Mermaid: [`module-08/mermaid/aws/m08-aws-rag-conceptual.mmd`](module-08/mermaid/aws/m08-aws-rag-conceptual.mmd)
- Draw.io: [`module-08/drawio/aws/m08-aws-rag-conceptual.drawio`](module-08/drawio/aws/m08-aws-rag-conceptual.drawio)
- SVG: [`module-08/svg/aws/m08-aws-rag-conceptual.svg`](module-08/svg/aws/m08-aws-rag-conceptual.svg)
- PNG: [`module-08/png/aws/m08-aws-rag-conceptual.png`](module-08/png/aws/m08-aws-rag-conceptual.png)

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
  Q["Query"] --> Retr["Retrieve"]
  Retr --> KB["Knowledge Sources"]
  Retr --> Gen["Generate via Bedrock"]
  Gen --> Ans["Grounded Answer"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
