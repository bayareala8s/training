# Pattern Selection Matrix Visual

| Field | Value |
| ----- | ----- |
| ID | `m06-aws-pattern-selection-matrix-visual` |
| Category | `aws` |
| Module | `module-06` |
| Lesson | 6.2 |
| Lab | lab-06 |
| Learning objective | Integration/data architecture: Pattern Selection Matrix Visual |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-06/mermaid/aws/m06-aws-pattern-selection-matrix-visual.mmd`](module-06/mermaid/aws/m06-aws-pattern-selection-matrix-visual.mmd)
- Draw.io: [`module-06/drawio/aws/m06-aws-pattern-selection-matrix-visual.drawio`](module-06/drawio/aws/m06-aws-pattern-selection-matrix-visual.drawio)
- SVG: [`module-06/svg/aws/m06-aws-pattern-selection-matrix-visual.svg`](module-06/svg/aws/m06-aws-pattern-selection-matrix-visual.svg)
- PNG: [`module-06/png/aws/m06-aws-pattern-selection-matrix-visual.png`](module-06/png/aws/m06-aws-pattern-selection-matrix-visual.png)

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
flowchart TB
  Need["Integration Need"] --> P{Latency · Coupling · Volume}
  P --> API["Sync API"]
  P --> Event["Events"]
  P --> Queue["Queues"]
  P --> File["Files / Batch"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
