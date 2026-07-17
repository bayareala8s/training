# Workflow Intelligence

| Field | Value |
| ----- | ----- |
| ID | `m08-aws-workflow-intelligence` |
| Category | `aws` |
| Module | `module-08` |
| Lesson | 8.1 |
| Lab | lab-08 |
| Learning objective | AI strategy: Workflow Intelligence |
| AWS icons | AWS Step Functions, Amazon Bedrock |

## Formats

- Mermaid: [`module-08/mermaid/aws/m08-aws-workflow-intelligence.mmd`](module-08/mermaid/aws/m08-aws-workflow-intelligence.mmd)
- Draw.io: [`module-08/drawio/aws/m08-aws-workflow-intelligence.drawio`](module-08/drawio/aws/m08-aws-workflow-intelligence.drawio)
- SVG: [`module-08/svg/aws/m08-aws-workflow-intelligence.svg`](module-08/svg/aws/m08-aws-workflow-intelligence.svg)
- PNG: [`module-08/png/aws/m08-aws-workflow-intelligence.png`](module-08/png/aws/m08-aws-workflow-intelligence.png)

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
  WF["Business Workflow"] --> DecPoints["Decision Points"]
  DecPoints --> AI["AI Suggestion"]
  AI --> Human["Human Accountable"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
