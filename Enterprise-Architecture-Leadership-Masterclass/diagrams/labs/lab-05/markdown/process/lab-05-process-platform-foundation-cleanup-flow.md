# Platform Foundation — Cleanup Flow

| Field | Value |
| ----- | ----- |
| ID | `lab-05-process-platform-foundation-cleanup-flow` |
| Category | `process` |
| Module | `lab-05` |
| Lesson | — |
| Lab | lab-05 |
| Learning objective | Lab 5 visual: Cleanup Flow |
| AWS icons | IAM, Amazon S3, AWS CloudTrail, Amazon CloudWatch, AWS Budgets, Amazon DynamoDB, AWS Lambda, Amazon API Gateway, AWS Systems Manager |

## Formats

- Mermaid: [`labs/lab-05/mermaid/process/lab-05-process-platform-foundation-cleanup-flow.mmd`](labs/lab-05/mermaid/process/lab-05-process-platform-foundation-cleanup-flow.mmd)
- Draw.io: [`labs/lab-05/drawio/process/lab-05-process-platform-foundation-cleanup-flow.drawio`](labs/lab-05/drawio/process/lab-05-process-platform-foundation-cleanup-flow.drawio)
- SVG: [`labs/lab-05/svg/process/lab-05-process-platform-foundation-cleanup-flow.svg`](labs/lab-05/svg/process/lab-05-process-platform-foundation-cleanup-flow.svg)
- PNG: [`labs/lab-05/png/process/lab-05-process-platform-foundation-cleanup-flow.png`](labs/lab-05/png/process/lab-05-process-platform-foundation-cleanup-flow.png)

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
  Done["Lab Done"] --> Destroy["terraform destroy / cleanup script"] --> Verify["Verify no lab tags remain"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
