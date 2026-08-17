# Platform Foundation — Failure Scenario

| Field | Value |
| ----- | ----- |
| ID | `lab-05-process-platform-foundation-failure-scenario` |
| Category | `process` |
| Module | `lab-05` |
| Lesson | — |
| Lab | lab-05 |
| Learning objective | Lab 5 visual: Failure Scenario |
| AWS icons | IAM, Amazon S3, AWS CloudTrail, Amazon CloudWatch, AWS Budgets, Amazon DynamoDB, AWS Lambda, Amazon API Gateway, AWS Systems Manager |

## Formats

- Mermaid: [`labs/lab-05/mermaid/process/lab-05-process-platform-foundation-failure-scenario.mmd`](labs/lab-05/mermaid/process/lab-05-process-platform-foundation-failure-scenario.mmd)
- Draw.io: [`labs/lab-05/drawio/process/lab-05-process-platform-foundation-failure-scenario.drawio`](labs/lab-05/drawio/process/lab-05-process-platform-foundation-failure-scenario.drawio)
- SVG: [`labs/lab-05/svg/process/lab-05-process-platform-foundation-failure-scenario.svg`](labs/lab-05/svg/process/lab-05-process-platform-foundation-failure-scenario.svg)
- PNG: [`labs/lab-05/png/process/lab-05-process-platform-foundation-failure-scenario.png`](labs/lab-05/png/process/lab-05-process-platform-foundation-failure-scenario.png)

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
  Fail["Failure Injected"] --> Detect["Detect"] --> Respond["Respond"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
