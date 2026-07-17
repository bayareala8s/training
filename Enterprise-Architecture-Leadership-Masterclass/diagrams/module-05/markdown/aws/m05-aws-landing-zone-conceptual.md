# Landing Zone Conceptual

| Field | Value |
| ----- | ----- |
| ID | `m05-aws-landing-zone-conceptual` |
| Category | `aws` |
| Module | `module-05` |
| Lesson | 5.2 |
| Lab | lab-05 |
| Learning objective | Cloud/platform strategy: Landing Zone Conceptual |
| AWS icons | AWS Organizations, IAM, CloudTrail, AWS Config |

## Formats

- Mermaid: [`module-05/mermaid/aws/m05-aws-landing-zone-conceptual.mmd`](module-05/mermaid/aws/m05-aws-landing-zone-conceptual.mmd)
- Draw.io: [`module-05/drawio/aws/m05-aws-landing-zone-conceptual.drawio`](module-05/drawio/aws/m05-aws-landing-zone-conceptual.drawio)
- SVG: [`module-05/svg/aws/m05-aws-landing-zone-conceptual.svg`](module-05/svg/aws/m05-aws-landing-zone-conceptual.svg)
- PNG: [`module-05/png/aws/m05-aws-landing-zone-conceptual.png`](module-05/png/aws/m05-aws-landing-zone-conceptual.png)

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
  LZ["Landing Zone"] --> Id["Identity Center / IAM"]
  LZ --> Log["Central Logging"]
  LZ --> Net["Network Baseline"]
  LZ --> Guard["Guardrails / SCPs"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
