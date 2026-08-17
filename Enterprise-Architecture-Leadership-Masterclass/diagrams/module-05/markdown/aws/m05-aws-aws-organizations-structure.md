# AWS Organizations Structure

| Field | Value |
| ----- | ----- |
| ID | `m05-aws-aws-organizations-structure` |
| Category | `aws` |
| Module | `module-05` |
| Lesson | 5.1 |
| Lab | lab-05 |
| Learning objective | Cloud/platform strategy: AWS Organizations Structure |
| AWS icons | AWS Organizations, IAM |

## Formats

- Mermaid: [`module-05/mermaid/aws/m05-aws-aws-organizations-structure.mmd`](module-05/mermaid/aws/m05-aws-aws-organizations-structure.mmd)
- Draw.io: [`module-05/drawio/aws/m05-aws-aws-organizations-structure.drawio`](module-05/drawio/aws/m05-aws-aws-organizations-structure.drawio)
- SVG: [`module-05/svg/aws/m05-aws-aws-organizations-structure.svg`](module-05/svg/aws/m05-aws-aws-organizations-structure.svg)
- PNG: [`module-05/png/aws/m05-aws-aws-organizations-structure.png`](module-05/png/aws/m05-aws-aws-organizations-structure.png)

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
  subgraph Org["AWS Organizations"]
    Mgmt["Management Account"]
    Sec["Security / Audit OU"]
    Shared["Shared Services OU"]
    Work["Workloads OU"]
    Sand["Sandbox OU"]
  end
  Mgmt --> Sec & Shared & Work & Sand
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
