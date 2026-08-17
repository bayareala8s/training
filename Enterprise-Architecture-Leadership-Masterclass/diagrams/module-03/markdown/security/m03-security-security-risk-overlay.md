# Security Risk Overlay

| Field | Value |
| ----- | ----- |
| ID | `m03-security-security-risk-overlay` |
| Category | `security` |
| Module | `module-03` |
| Lesson | 3.1 |
| Lab | lab-03 |
| Learning objective | Assess current estate: Security Risk Overlay |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-03/mermaid/security/m03-security-security-risk-overlay.mmd`](module-03/mermaid/security/m03-security-security-risk-overlay.mmd)
- Draw.io: [`module-03/drawio/security/m03-security-security-risk-overlay.drawio`](module-03/drawio/security/m03-security-security-risk-overlay.drawio)
- SVG: [`module-03/svg/security/m03-security-security-risk-overlay.svg`](module-03/svg/security/m03-security-security-risk-overlay.svg)
- PNG: [`module-03/png/security/m03-security-security-risk-overlay.png`](module-03/png/security/m03-security-security-risk-overlay.png)

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
  Apps["Apps with High Security Risk"] --> Id["Inconsistent Identity"]
  Apps --> Enc["Uneven Encryption"]
  Apps --> Priv["Excess Privilege"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
