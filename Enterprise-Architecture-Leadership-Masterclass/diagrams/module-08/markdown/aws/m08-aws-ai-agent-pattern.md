# AI Agent Pattern

| Field | Value |
| ----- | ----- |
| ID | `m08-aws-ai-agent-pattern` |
| Category | `aws` |
| Module | `module-08` |
| Lesson | 8.4 |
| Lab | lab-08 |
| Learning objective | AI strategy: AI Agent Pattern |
| AWS icons | Amazon Bedrock, AWS Step Functions |

## Formats

- Mermaid: [`module-08/mermaid/aws/m08-aws-ai-agent-pattern.mmd`](module-08/mermaid/aws/m08-aws-ai-agent-pattern.mmd)
- Draw.io: [`module-08/drawio/aws/m08-aws-ai-agent-pattern.drawio`](module-08/drawio/aws/m08-aws-ai-agent-pattern.drawio)
- SVG: [`module-08/svg/aws/m08-aws-ai-agent-pattern.svg`](module-08/svg/aws/m08-aws-ai-agent-pattern.svg)
- PNG: [`module-08/png/aws/m08-aws-ai-agent-pattern.png`](module-08/png/aws/m08-aws-ai-agent-pattern.png)

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
  Goal["Goal"] --> Agent["Agent Loop"]
  Agent --> Tools["Tools / APIs"]
  Agent --> HITL["HITL Checkpoints"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
