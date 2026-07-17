# STRIDE Threat Overlay

| Field | Value |
| ----- | ----- |
| ID | `m07-security-stride-threat-overlay` |
| Category | `security` |
| Module | `module-07` |
| Lesson | 7.4 |
| Lab | lab-07 |
| Learning objective | Security/resilience: STRIDE Threat Overlay |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-07/mermaid/security/m07-security-stride-threat-overlay.mmd`](module-07/mermaid/security/m07-security-stride-threat-overlay.mmd)
- Draw.io: [`module-07/drawio/security/m07-security-stride-threat-overlay.drawio`](module-07/drawio/security/m07-security-stride-threat-overlay.drawio)
- SVG: [`module-07/svg/security/m07-security-stride-threat-overlay.svg`](module-07/svg/security/m07-security-stride-threat-overlay.svg)
- PNG: [`module-07/png/security/m07-security-stride-threat-overlay.png`](module-07/png/security/m07-security-stride-threat-overlay.png)

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
  S["Spoofing"] --- T["Tampering"]
  R["Repudiation"] --- I["Info Disclosure"]
  D["DoS"] --- E["Elevation"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
