# Network Segmentation Conceptual

| Field | Value |
| ----- | ----- |
| ID | `m07-security-network-segmentation-conceptual` |
| Category | `security` |
| Module | `module-07` |
| Lesson | 7.3 |
| Lab | lab-07 |
| Learning objective | Security/resilience: Network Segmentation Conceptual |
| AWS icons | Amazon VPC |

## Formats

- Mermaid: [`module-07/mermaid/security/m07-security-network-segmentation-conceptual.mmd`](module-07/mermaid/security/m07-security-network-segmentation-conceptual.mmd)
- Draw.io: [`module-07/drawio/security/m07-security-network-segmentation-conceptual.drawio`](module-07/drawio/security/m07-security-network-segmentation-conceptual.drawio)
- SVG: [`module-07/svg/security/m07-security-network-segmentation-conceptual.svg`](module-07/svg/security/m07-security-network-segmentation-conceptual.svg)
- PNG: [`module-07/png/security/m07-security-network-segmentation-conceptual.png`](module-07/png/security/m07-security-network-segmentation-conceptual.png)

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
  Pub["Public Subnet"] --> Priv["Private Subnet"]
  Priv --> Data["Data Subnet"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
