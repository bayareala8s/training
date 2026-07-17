# Lab 8 Mock vs Bedrock

| Field | Value |
| ----- | ----- |
| ID | `m08-aws-lab-8-mock-vs-bedrock` |
| Category | `aws` |
| Module | `module-08` |
| Lesson | 8.1 |
| Lab | lab-08 |
| Learning objective | AI strategy: Lab 8 Mock vs Bedrock |
| AWS icons | Amazon Bedrock, AWS Lambda |

## Formats

- Mermaid: [`module-08/mermaid/aws/m08-aws-lab-8-mock-vs-bedrock.mmd`](module-08/mermaid/aws/m08-aws-lab-8-mock-vs-bedrock.mmd)
- Draw.io: [`module-08/drawio/aws/m08-aws-lab-8-mock-vs-bedrock.drawio`](module-08/drawio/aws/m08-aws-lab-8-mock-vs-bedrock.drawio)
- SVG: [`module-08/svg/aws/m08-aws-lab-8-mock-vs-bedrock.svg`](module-08/svg/aws/m08-aws-lab-8-mock-vs-bedrock.svg)
- PNG: [`module-08/png/aws/m08-aws-lab-8-mock-vs-bedrock.png`](module-08/png/aws/m08-aws-lab-8-mock-vs-bedrock.png)

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
  Flag{"use_mock_bedrock?"}
  Flag -->|true| Mock["Deterministic Mock JSON"]
  Flag -->|false| BR["Amazon Bedrock"]
  Mock & BR --> Validate["Validate + Rules"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
