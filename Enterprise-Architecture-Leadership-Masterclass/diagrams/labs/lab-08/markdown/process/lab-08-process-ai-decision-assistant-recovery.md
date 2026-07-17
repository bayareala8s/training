# AI Decision Assistant — Recovery

| Field | Value |
| ----- | ----- |
| ID | `lab-08-process-ai-decision-assistant-recovery` |
| Category | `process` |
| Module | `lab-08` |
| Lesson | — |
| Lab | lab-08 |
| Learning objective | Lab 8 visual: Recovery |
| AWS icons | Amazon Bedrock, AWS Lambda, AWS Step Functions, Amazon DynamoDB, Amazon API Gateway, Amazon CloudWatch |

## Formats

- Mermaid: [`labs/lab-08/mermaid/process/lab-08-process-ai-decision-assistant-recovery.mmd`](labs/lab-08/mermaid/process/lab-08-process-ai-decision-assistant-recovery.mmd)
- Draw.io: [`labs/lab-08/drawio/process/lab-08-process-ai-decision-assistant-recovery.drawio`](labs/lab-08/drawio/process/lab-08-process-ai-decision-assistant-recovery.drawio)
- SVG: [`labs/lab-08/svg/process/lab-08-process-ai-decision-assistant-recovery.svg`](labs/lab-08/svg/process/lab-08-process-ai-decision-assistant-recovery.svg)
- PNG: [`labs/lab-08/png/process/lab-08-process-ai-decision-assistant-recovery.png`](labs/lab-08/png/process/lab-08-process-ai-decision-assistant-recovery.png)

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
