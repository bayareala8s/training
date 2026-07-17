# Data Classification Overlay

| Field | Value |
| ----- | ----- |
| ID | `m07-security-data-classification-overlay` |
| Category | `security` |
| Module | `module-07` |
| Lesson | 7.2 |
| Lab | lab-07 |
| Learning objective | Security/resilience: Data Classification Overlay |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-07/mermaid/security/m07-security-data-classification-overlay.mmd`](module-07/mermaid/security/m07-security-data-classification-overlay.mmd)
- Draw.io: [`module-07/drawio/security/m07-security-data-classification-overlay.drawio`](module-07/drawio/security/m07-security-data-classification-overlay.drawio)
- SVG: [`module-07/svg/security/m07-security-data-classification-overlay.svg`](module-07/svg/security/m07-security-data-classification-overlay.svg)
- PNG: [`module-07/png/security/m07-security-data-classification-overlay.png`](module-07/png/security/m07-security-data-classification-overlay.png)

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
  Pub["Public"] --> Int["Internal"]
  Int --> Conf["Confidential"]
  Conf --> Res["Restricted"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
