# Model Evaluation Loop

| Field | Value |
| ----- | ----- |
| ID | `m08-aws-model-evaluation-loop` |
| Category | `aws` |
| Module | `module-08` |
| Lesson | 8.1 |
| Lab | lab-08 |
| Learning objective | AI strategy: Model Evaluation Loop |
| AWS icons | Amazon S3, Amazon CloudWatch |

## Formats

- Mermaid: [`module-08/mermaid/aws/m08-aws-model-evaluation-loop.mmd`](module-08/mermaid/aws/m08-aws-model-evaluation-loop.mmd)
- Draw.io: [`module-08/drawio/aws/m08-aws-model-evaluation-loop.drawio`](module-08/drawio/aws/m08-aws-model-evaluation-loop.drawio)
- SVG: [`module-08/svg/aws/m08-aws-model-evaluation-loop.svg`](module-08/svg/aws/m08-aws-model-evaluation-loop.svg)
- PNG: [`module-08/png/aws/m08-aws-model-evaluation-loop.png`](module-08/png/aws/m08-aws-model-evaluation-loop.png)

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
  Set["Eval Dataset"] --> Run["Run Cases"]
  Run --> Score["Quality Scores"]
  Score --> Dec["Ship / Fix / Block"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
