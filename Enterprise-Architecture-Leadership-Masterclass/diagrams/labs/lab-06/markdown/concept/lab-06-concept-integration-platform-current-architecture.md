# Integration Platform — Current Architecture

| Field | Value |
| ----- | ----- |
| ID | `lab-06-concept-integration-platform-current-architecture` |
| Category | `concept` |
| Module | `lab-06` |
| Lesson | — |
| Lab | lab-06 |
| Learning objective | Lab 6 visual: Current Architecture |
| AWS icons | Amazon API Gateway, AWS Lambda, Amazon EventBridge, Amazon SQS, AWS Step Functions, Amazon S3, Amazon DynamoDB, Amazon SNS |

## Formats

- Mermaid: [`labs/lab-06/mermaid/concept/lab-06-concept-integration-platform-current-architecture.mmd`](labs/lab-06/mermaid/concept/lab-06-concept-integration-platform-current-architecture.mmd)
- Draw.io: [`labs/lab-06/drawio/concept/lab-06-concept-integration-platform-current-architecture.drawio`](labs/lab-06/drawio/concept/lab-06-concept-integration-platform-current-architecture.drawio)
- SVG: [`labs/lab-06/svg/concept/lab-06-concept-integration-platform-current-architecture.svg`](labs/lab-06/svg/concept/lab-06-concept-integration-platform-current-architecture.svg)
- PNG: [`labs/lab-06/png/concept/lab-06-concept-integration-platform-current-architecture.png`](labs/lab-06/png/concept/lab-06-concept-integration-platform-current-architecture.png)

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
  AsIs["As-Is Fragmented"] --> Pain["Pain: Cost · Risk · Slow"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
