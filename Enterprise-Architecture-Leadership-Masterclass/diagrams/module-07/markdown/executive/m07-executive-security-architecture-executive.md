# Security Architecture Executive

| Field | Value |
| ----- | ----- |
| ID | `m07-executive-security-architecture-executive` |
| Category | `executive` |
| Module | `module-07` |
| Lesson | 7.1 |
| Lab | lab-07 |
| Learning objective | Security/resilience: Security Architecture Executive |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-07/mermaid/executive/m07-executive-security-architecture-executive.mmd`](module-07/mermaid/executive/m07-executive-security-architecture-executive.mmd)
- Draw.io: [`module-07/drawio/executive/m07-executive-security-architecture-executive.drawio`](module-07/drawio/executive/m07-executive-security-architecture-executive.drawio)
- SVG: [`module-07/svg/executive/m07-executive-security-architecture-executive.svg`](module-07/svg/executive/m07-executive-security-architecture-executive.svg)
- PNG: [`module-07/png/executive/m07-executive-security-architecture-executive.png`](module-07/png/executive/m07-executive-security-architecture-executive.png)

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
  Trust["Zero Trust Direction"] --> Id["Identity First"]
  Trust --> Data["Protect Data"]
  Trust --> Det["Detect & Recover"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
