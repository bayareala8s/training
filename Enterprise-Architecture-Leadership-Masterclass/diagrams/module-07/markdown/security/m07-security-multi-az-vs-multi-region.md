# Multi-AZ vs Multi-Region

| Field | Value |
| ----- | ----- |
| ID | `m07-security-multi-az-vs-multi-region` |
| Category | `security` |
| Module | `module-07` |
| Lesson | 7.3 |
| Lab | lab-07 |
| Learning objective | Security/resilience: Multi-AZ vs Multi-Region |
| AWS icons | Amazon S3, Amazon DynamoDB |

## Formats

- Mermaid: [`module-07/mermaid/security/m07-security-multi-az-vs-multi-region.mmd`](module-07/mermaid/security/m07-security-multi-az-vs-multi-region.mmd)
- Draw.io: [`module-07/drawio/security/m07-security-multi-az-vs-multi-region.drawio`](module-07/drawio/security/m07-security-multi-az-vs-multi-region.drawio)
- SVG: [`module-07/svg/security/m07-security-multi-az-vs-multi-region.svg`](module-07/svg/security/m07-security-multi-az-vs-multi-region.svg)
- PNG: [`module-07/png/security/m07-security-multi-az-vs-multi-region.png`](module-07/png/security/m07-security-multi-az-vs-multi-region.png)

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
  AZ["Multi-AZ<br/>Default resilience"] --- Reg["Multi-Region<br/>Higher cost/complexity"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
