# Integration Platform — Recovery

| Field | Value |
| ----- | ----- |
| ID | `lab-06-process-integration-platform-recovery` |
| Category | `process` |
| Module | `lab-06` |
| Lesson | — |
| Lab | lab-06 |
| Learning objective | Lab 6 visual: Recovery |
| AWS icons | Amazon API Gateway, AWS Lambda, Amazon EventBridge, Amazon SQS, AWS Step Functions, Amazon S3, Amazon DynamoDB, Amazon SNS |

## Formats

- Mermaid: [`labs/lab-06/mermaid/process/lab-06-process-integration-platform-recovery.mmd`](labs/lab-06/mermaid/process/lab-06-process-integration-platform-recovery.mmd)
- Draw.io: [`labs/lab-06/drawio/process/lab-06-process-integration-platform-recovery.drawio`](labs/lab-06/drawio/process/lab-06-process-integration-platform-recovery.drawio)
- SVG: [`labs/lab-06/svg/process/lab-06-process-integration-platform-recovery.svg`](labs/lab-06/svg/process/lab-06-process-integration-platform-recovery.svg)
- PNG: [`labs/lab-06/png/process/lab-06-process-integration-platform-recovery.png`](labs/lab-06/png/process/lab-06-process-integration-platform-recovery.png)

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
  Detect --> Recover["Recover / Restore"] --> Confirm["Confirm RTO/RPO"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
