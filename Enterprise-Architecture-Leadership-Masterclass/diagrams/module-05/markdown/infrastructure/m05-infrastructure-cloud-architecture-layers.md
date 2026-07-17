# Cloud Architecture Layers

| Field | Value |
| ----- | ----- |
| ID | `m05-infrastructure-cloud-architecture-layers` |
| Category | `infrastructure` |
| Module | `module-05` |
| Lesson | 5.2 |
| Lab | lab-05 |
| Learning objective | Cloud/platform strategy: Cloud Architecture Layers |
| AWS icons | Amazon VPC, IAM |

## Formats

- Mermaid: [`module-05/mermaid/infrastructure/m05-infrastructure-cloud-architecture-layers.mmd`](module-05/mermaid/infrastructure/m05-infrastructure-cloud-architecture-layers.mmd)
- Draw.io: [`module-05/drawio/infrastructure/m05-infrastructure-cloud-architecture-layers.drawio`](module-05/drawio/infrastructure/m05-infrastructure-cloud-architecture-layers.drawio)
- SVG: [`module-05/svg/infrastructure/m05-infrastructure-cloud-architecture-layers.svg`](module-05/svg/infrastructure/m05-infrastructure-cloud-architecture-layers.svg)
- PNG: [`module-05/png/infrastructure/m05-infrastructure-cloud-architecture-layers.png`](module-05/png/infrastructure/m05-infrastructure-cloud-architecture-layers.png)

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
  Edge["Edge / DNS"] --> Net["Network"]
  Net --> Comp["Compute / App"]
  Comp --> Data["Data"]
  Net & Comp & Data --> Sec["Security Controls"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
