# Idempotency Pattern

| Field | Value |
| ----- | ----- |
| ID | `m06-aws-idempotency-pattern` |
| Category | `aws` |
| Module | `module-06` |
| Lesson | 6.4 |
| Lab | lab-06 |
| Learning objective | Integration/data architecture: Idempotency Pattern |
| AWS icons | Amazon DynamoDB, AWS Lambda |

## Formats

- Mermaid: [`module-06/mermaid/aws/m06-aws-idempotency-pattern.mmd`](module-06/mermaid/aws/m06-aws-idempotency-pattern.mmd)
- Draw.io: [`module-06/drawio/aws/m06-aws-idempotency-pattern.drawio`](module-06/drawio/aws/m06-aws-idempotency-pattern.drawio)
- SVG: [`module-06/svg/aws/m06-aws-idempotency-pattern.svg`](module-06/svg/aws/m06-aws-idempotency-pattern.svg)
- PNG: [`module-06/png/aws/m06-aws-idempotency-pattern.png`](module-06/png/aws/m06-aws-idempotency-pattern.png)

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
  Ev["Event"] --> L["Lambda"]
  L --> DDB["Idempotency Table"]
  DDB -->|duplicate| Skip["Skip"]
  DDB -->|new| Proc["Process"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
