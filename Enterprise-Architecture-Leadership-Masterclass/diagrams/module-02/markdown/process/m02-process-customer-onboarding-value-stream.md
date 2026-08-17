# Customer Onboarding Value Stream

| Field | Value |
| ----- | ----- |
| ID | `m02-process-customer-onboarding-value-stream` |
| Category | `process` |
| Module | `module-02` |
| Lesson | 2.4 |
| Lab | — |
| Learning objective | Apply business architecture visual: Customer Onboarding Value Stream |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-02/mermaid/process/m02-process-customer-onboarding-value-stream.mmd`](module-02/mermaid/process/m02-process-customer-onboarding-value-stream.mmd)
- Draw.io: [`module-02/drawio/process/m02-process-customer-onboarding-value-stream.drawio`](module-02/drawio/process/m02-process-customer-onboarding-value-stream.drawio)
- SVG: [`module-02/svg/process/m02-process-customer-onboarding-value-stream.svg`](module-02/svg/process/m02-process-customer-onboarding-value-stream.svg)
- PNG: [`module-02/png/process/m02-process-customer-onboarding-value-stream.png`](module-02/png/process/m02-process-customer-onboarding-value-stream.png)

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
  A["Acquire"] --> B["Verify Identity"]
  B --> C["Risk Decision"]
  C --> D["Open Account"]
  D --> E["Activate Products"]
  E --> F["Ongoing Service"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
