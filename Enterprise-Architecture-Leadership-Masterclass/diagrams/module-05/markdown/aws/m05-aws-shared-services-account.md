# Shared Services Account

| Field | Value |
| ----- | ----- |
| ID | `m05-aws-shared-services-account` |
| Category | `aws` |
| Module | `module-05` |
| Lesson | 5.4 |
| Lab | lab-05 |
| Learning objective | Cloud/platform strategy: Shared Services Account |
| AWS icons | Amazon S3, AWS Lambda, AWS Systems Manager |

## Formats

- Mermaid: [`module-05/mermaid/aws/m05-aws-shared-services-account.mmd`](module-05/mermaid/aws/m05-aws-shared-services-account.mmd)
- Draw.io: [`module-05/drawio/aws/m05-aws-shared-services-account.drawio`](module-05/drawio/aws/m05-aws-shared-services-account.drawio)
- SVG: [`module-05/svg/aws/m05-aws-shared-services-account.svg`](module-05/svg/aws/m05-aws-shared-services-account.svg)
- PNG: [`module-05/png/aws/m05-aws-shared-services-account.png`](module-05/png/aws/m05-aws-shared-services-account.png)

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
  Shared["Shared Services Account"] --> Art["Artifacts / Params"]
  Shared --> Log["Log Archive"]
  Shared --> Net["Network Hub"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
