# Bedrock Decision Assistant

| Field | Value |
| ----- | ----- |
| ID | `m08-aws-bedrock-decision-assistant` |
| Category | `aws` |
| Module | `module-08` |
| Lesson | 8.2 |
| Lab | lab-08 |
| Learning objective | AI strategy: Bedrock Decision Assistant |
| AWS icons | Amazon Bedrock, AWS Lambda, AWS Step Functions, Amazon DynamoDB |

## Formats

- Mermaid: [`module-08/mermaid/aws/m08-aws-bedrock-decision-assistant.mmd`](module-08/mermaid/aws/m08-aws-bedrock-decision-assistant.mmd)
- Draw.io: [`module-08/drawio/aws/m08-aws-bedrock-decision-assistant.drawio`](module-08/drawio/aws/m08-aws-bedrock-decision-assistant.drawio)
- SVG: [`module-08/svg/aws/m08-aws-bedrock-decision-assistant.svg`](module-08/svg/aws/m08-aws-bedrock-decision-assistant.svg)
- PNG: [`module-08/png/aws/m08-aws-bedrock-decision-assistant.png`](module-08/png/aws/m08-aws-bedrock-decision-assistant.png)

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
  Inc["Incident"] --> API["API Gateway"]
  API --> L["Lambda"]
  L --> BR["Bedrock"]
  L --> Rules["Deterministic Rules"]
  Rules --> SF["Step Functions HITL"]
  L --> DDB["Audit DynamoDB"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
