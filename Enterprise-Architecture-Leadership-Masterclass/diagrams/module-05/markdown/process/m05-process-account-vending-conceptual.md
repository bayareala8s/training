# Account Vending Conceptual

| Field | Value |
| ----- | ----- |
| ID | `m05-process-account-vending-conceptual` |
| Category | `process` |
| Module | `module-05` |
| Lesson | 5.3 |
| Lab | lab-05 |
| Learning objective | Cloud/platform strategy: Account Vending Conceptual |
| AWS icons | AWS Organizations |

## Formats

- Mermaid: [`module-05/mermaid/process/m05-process-account-vending-conceptual.mmd`](module-05/mermaid/process/m05-process-account-vending-conceptual.mmd)
- Draw.io: [`module-05/drawio/process/m05-process-account-vending-conceptual.drawio`](module-05/drawio/process/m05-process-account-vending-conceptual.drawio)
- SVG: [`module-05/svg/process/m05-process-account-vending-conceptual.svg`](module-05/svg/process/m05-process-account-vending-conceptual.svg)
- PNG: [`module-05/png/process/m05-process-account-vending-conceptual.png`](module-05/png/process/m05-process-account-vending-conceptual.png)

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
  Req["Request Account"] --> Approve["Approve"]
  Approve --> Prov["Provision Baseline"]
  Prov --> Handoff["Handoff to Team"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
