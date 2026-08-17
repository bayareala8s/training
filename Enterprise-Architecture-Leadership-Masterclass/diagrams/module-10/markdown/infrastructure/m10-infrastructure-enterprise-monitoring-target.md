# Enterprise Monitoring Target

| Field | Value |
| ----- | ----- |
| ID | `m10-infrastructure-enterprise-monitoring-target` |
| Category | `infrastructure` |
| Module | `module-10` |
| Lesson | 10.1 |
| Lab | lab-10 |
| Learning objective | Capstone visual: Enterprise Monitoring Target |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-10/mermaid/infrastructure/m10-infrastructure-enterprise-monitoring-target.mmd`](module-10/mermaid/infrastructure/m10-infrastructure-enterprise-monitoring-target.mmd)
- Draw.io: [`module-10/drawio/infrastructure/m10-infrastructure-enterprise-monitoring-target.drawio`](module-10/drawio/infrastructure/m10-infrastructure-enterprise-monitoring-target.drawio)
- SVG: [`module-10/svg/infrastructure/m10-infrastructure-enterprise-monitoring-target.svg`](module-10/svg/infrastructure/m10-infrastructure-enterprise-monitoring-target.svg)
- PNG: [`module-10/png/infrastructure/m10-infrastructure-enterprise-monitoring-target.png`](module-10/png/infrastructure/m10-infrastructure-enterprise-monitoring-target.png)

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
  Apps --> CloudWatch
  Apps --> CloudTrail
  CloudWatch --> Alarms
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
