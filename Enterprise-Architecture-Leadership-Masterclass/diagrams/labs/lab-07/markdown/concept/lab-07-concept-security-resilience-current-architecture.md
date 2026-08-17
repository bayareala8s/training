# Security Resilience — Current Architecture

| Field | Value |
| ----- | ----- |
| ID | `lab-07-concept-security-resilience-current-architecture` |
| Category | `concept` |
| Module | `lab-07` |
| Lesson | — |
| Lab | lab-07 |
| Learning objective | Lab 7 visual: Current Architecture |
| AWS icons | IAM, AWS KMS, Amazon S3, Amazon CloudWatch |

## Formats

- Mermaid: [`labs/lab-07/mermaid/concept/lab-07-concept-security-resilience-current-architecture.mmd`](labs/lab-07/mermaid/concept/lab-07-concept-security-resilience-current-architecture.mmd)
- Draw.io: [`labs/lab-07/drawio/concept/lab-07-concept-security-resilience-current-architecture.drawio`](labs/lab-07/drawio/concept/lab-07-concept-security-resilience-current-architecture.drawio)
- SVG: [`labs/lab-07/svg/concept/lab-07-concept-security-resilience-current-architecture.svg`](labs/lab-07/svg/concept/lab-07-concept-security-resilience-current-architecture.svg)
- PNG: [`labs/lab-07/png/concept/lab-07-concept-security-resilience-current-architecture.png`](labs/lab-07/png/concept/lab-07-concept-security-resilience-current-architecture.png)

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
