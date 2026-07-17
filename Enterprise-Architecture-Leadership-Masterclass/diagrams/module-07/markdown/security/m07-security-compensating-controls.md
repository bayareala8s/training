# Compensating Controls

| Field | Value |
| ----- | ----- |
| ID | `m07-security-compensating-controls` |
| Category | `security` |
| Module | `module-07` |
| Lesson | 7.1 |
| Lab | lab-07 |
| Learning objective | Security/resilience: Compensating Controls |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-07/mermaid/security/m07-security-compensating-controls.mmd`](module-07/mermaid/security/m07-security-compensating-controls.mmd)
- Draw.io: [`module-07/drawio/security/m07-security-compensating-controls.drawio`](module-07/drawio/security/m07-security-compensating-controls.drawio)
- SVG: [`module-07/svg/security/m07-security-compensating-controls.svg`](module-07/svg/security/m07-security-compensating-controls.svg)
- PNG: [`module-07/png/security/m07-security-compensating-controls.png`](module-07/png/security/m07-security-compensating-controls.png)

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
  Gap["Control Gap"] --> Comp["Compensating Control"]
  Comp --> Expiry["Time-boxed Review"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
