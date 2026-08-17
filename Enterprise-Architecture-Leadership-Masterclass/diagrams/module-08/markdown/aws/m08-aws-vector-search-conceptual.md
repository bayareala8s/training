# Vector Search Conceptual

| Field | Value |
| ----- | ----- |
| ID | `m08-aws-vector-search-conceptual` |
| Category | `aws` |
| Module | `module-08` |
| Lesson | 8.1 |
| Lab | lab-08 |
| Learning objective | AI strategy: Vector Search Conceptual |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-08/mermaid/aws/m08-aws-vector-search-conceptual.mmd`](module-08/mermaid/aws/m08-aws-vector-search-conceptual.mmd)
- Draw.io: [`module-08/drawio/aws/m08-aws-vector-search-conceptual.drawio`](module-08/drawio/aws/m08-aws-vector-search-conceptual.drawio)
- SVG: [`module-08/svg/aws/m08-aws-vector-search-conceptual.svg`](module-08/svg/aws/m08-aws-vector-search-conceptual.svg)
- PNG: [`module-08/png/aws/m08-aws-vector-search-conceptual.png`](module-08/png/aws/m08-aws-vector-search-conceptual.png)

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
  Doc["Documents"] --> Emb["Embeddings"]
  Emb --> Vec["Vector Index (conceptual)"]
  Q["Query"] --> Vec --> Ctx["Top-K Context"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
