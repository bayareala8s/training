# Zero Trust Overview

| Field | Value |
| ----- | ----- |
| ID | `m07-security-zero-trust-overview` |
| Category | `security` |
| Module | `module-07` |
| Lesson | 7.1 |
| Lab | lab-07 |
| Learning objective | Security/resilience: Zero Trust Overview |
| AWS icons | IAM, Amazon VPC |

## Formats

- Mermaid: [`module-07/mermaid/security/m07-security-zero-trust-overview.mmd`](module-07/mermaid/security/m07-security-zero-trust-overview.mmd)
- Draw.io: [`module-07/drawio/security/m07-security-zero-trust-overview.drawio`](module-07/drawio/security/m07-security-zero-trust-overview.drawio)
- SVG: [`module-07/svg/security/m07-security-zero-trust-overview.svg`](module-07/svg/security/m07-security-zero-trust-overview.svg)
- PNG: [`module-07/png/security/m07-security-zero-trust-overview.png`](module-07/png/security/m07-security-zero-trust-overview.png)

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
  User["User / Service"] --> Verify["Verify Explicitly"]
  Verify --> Least["Least Privilege"]
  Least --> Assume["Assume Breach"]
  Assume --> Monitor["Continuous Monitoring"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
