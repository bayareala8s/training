# RTO RPO Targets

| Field | Value |
| ----- | ----- |
| ID | `m07-security-rto-rpo-targets` |
| Category | `security` |
| Module | `module-07` |
| Lesson | 7.2 |
| Lab | lab-07 |
| Learning objective | Security/resilience: RTO RPO Targets |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-07/mermaid/security/m07-security-rto-rpo-targets.mmd`](module-07/mermaid/security/m07-security-rto-rpo-targets.mmd)
- Draw.io: [`module-07/drawio/security/m07-security-rto-rpo-targets.drawio`](module-07/drawio/security/m07-security-rto-rpo-targets.drawio)
- SVG: [`module-07/svg/security/m07-security-rto-rpo-targets.svg`](module-07/svg/security/m07-security-rto-rpo-targets.svg)
- PNG: [`module-07/png/security/m07-security-rto-rpo-targets.png`](module-07/png/security/m07-security-rto-rpo-targets.png)

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
  Biz["Business Impact"] --> RTO["RTO Target"]
  Biz --> RPO["RPO Target"]
  RTO & RPO --> Strat["Recovery Strategy"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
