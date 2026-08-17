# Prompt Flow Structured JSON

| Field | Value |
| ----- | ----- |
| ID | `m08-aws-prompt-flow-structured-json` |
| Category | `aws` |
| Module | `module-08` |
| Lesson | 8.2 |
| Lab | lab-08 |
| Learning objective | AI strategy: Prompt Flow Structured JSON |
| AWS icons | Amazon Bedrock, AWS Lambda |

## Formats

- Mermaid: [`module-08/mermaid/aws/m08-aws-prompt-flow-structured-json.mmd`](module-08/mermaid/aws/m08-aws-prompt-flow-structured-json.mmd)
- Draw.io: [`module-08/drawio/aws/m08-aws-prompt-flow-structured-json.drawio`](module-08/drawio/aws/m08-aws-prompt-flow-structured-json.drawio)
- SVG: [`module-08/svg/aws/m08-aws-prompt-flow-structured-json.svg`](module-08/svg/aws/m08-aws-prompt-flow-structured-json.svg)
- PNG: [`module-08/png/aws/m08-aws-prompt-flow-structured-json.png`](module-08/png/aws/m08-aws-prompt-flow-structured-json.png)

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
  In["Input"] --> Prompt["Structured Prompt"]
  Prompt --> Model["Bedrock"]
  Model --> JSON["JSON Schema Validate"]
  JSON --> Out["Typed Decision"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
