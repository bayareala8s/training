# REST API Request Flow

| Field | Value |
| ----- | ----- |
| ID | `m06-sequence-rest-api-request-flow` |
| Category | `sequence` |
| Module | `module-06` |
| Lesson | 6.2 |
| Lab | lab-06 |
| Learning objective | Integration/data architecture: REST API Request Flow |
| AWS icons | Amazon API Gateway, AWS Lambda, Amazon DynamoDB |

## Formats

- Mermaid: [`module-06/mermaid/sequence/m06-sequence-rest-api-request-flow.mmd`](module-06/mermaid/sequence/m06-sequence-rest-api-request-flow.mmd)
- Draw.io: [`module-06/drawio/sequence/m06-sequence-rest-api-request-flow.drawio`](module-06/drawio/sequence/m06-sequence-rest-api-request-flow.drawio)
- SVG: [`module-06/svg/sequence/m06-sequence-rest-api-request-flow.svg`](module-06/svg/sequence/m06-sequence-rest-api-request-flow.svg)
- PNG: [`module-06/png/sequence/m06-sequence-rest-api-request-flow.png`](module-06/png/sequence/m06-sequence-rest-api-request-flow.png)

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
sequenceDiagram
  participant C as Client
  participant A as API Gateway
  participant L as Lambda
  participant D as DynamoDB
  C->>A: HTTPS request
  A->>L: Invoke
  L->>D: Get/Put item
  D-->>L: Result
  L-->>A: JSON response
  A-->>C: 200 OK
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
