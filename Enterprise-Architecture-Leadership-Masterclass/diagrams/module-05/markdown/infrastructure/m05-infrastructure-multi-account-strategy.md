# Multi-Account Strategy

| Field | Value |
| ----- | ----- |
| ID | `m05-infrastructure-multi-account-strategy` |
| Category | `infrastructure` |
| Module | `module-05` |
| Lesson | 5.3 |
| Lab | lab-05 |
| Learning objective | Cloud/platform strategy: Multi-Account Strategy |
| AWS icons | AWS Organizations |

## Formats

- Mermaid: [`module-05/mermaid/infrastructure/m05-infrastructure-multi-account-strategy.mmd`](module-05/mermaid/infrastructure/m05-infrastructure-multi-account-strategy.mmd)
- Draw.io: [`module-05/drawio/infrastructure/m05-infrastructure-multi-account-strategy.drawio`](module-05/drawio/infrastructure/m05-infrastructure-multi-account-strategy.drawio)
- SVG: [`module-05/svg/infrastructure/m05-infrastructure-multi-account-strategy.svg`](module-05/svg/infrastructure/m05-infrastructure-multi-account-strategy.svg)
- PNG: [`module-05/png/infrastructure/m05-infrastructure-multi-account-strategy.png`](module-05/png/infrastructure/m05-infrastructure-multi-account-strategy.png)

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
  Dev["Dev Account"] --> Test["Test Account"]
  Test --> Prod["Prod Account"]
  Shared["Shared Services"] --- Dev & Test & Prod
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
