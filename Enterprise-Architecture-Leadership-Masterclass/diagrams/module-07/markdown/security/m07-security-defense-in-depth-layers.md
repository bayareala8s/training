# Defense in Depth Layers

| Field | Value |
| ----- | ----- |
| ID | `m07-security-defense-in-depth-layers` |
| Category | `security` |
| Module | `module-07` |
| Lesson | 7.2 |
| Lab | lab-07 |
| Learning objective | Security/resilience: Defense in Depth Layers |
| AWS icons | AWS WAF, IAM, AWS KMS |

## Formats

- Mermaid: [`module-07/mermaid/security/m07-security-defense-in-depth-layers.mmd`](module-07/mermaid/security/m07-security-defense-in-depth-layers.mmd)
- Draw.io: [`module-07/drawio/security/m07-security-defense-in-depth-layers.drawio`](module-07/drawio/security/m07-security-defense-in-depth-layers.drawio)
- SVG: [`module-07/svg/security/m07-security-defense-in-depth-layers.svg`](module-07/svg/security/m07-security-defense-in-depth-layers.svg)
- PNG: [`module-07/png/security/m07-security-defense-in-depth-layers.png`](module-07/png/security/m07-security-defense-in-depth-layers.png)

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
  Edge["Edge WAF / Shield"] --> Net["Network Segmentation"]
  Net --> Id["Identity"]
  Id --> App["App Controls"]
  App --> Data["Data Encryption"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
