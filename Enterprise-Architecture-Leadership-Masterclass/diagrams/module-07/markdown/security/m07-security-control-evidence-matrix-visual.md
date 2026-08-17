# Control Evidence Matrix Visual

| Field | Value |
| ----- | ----- |
| ID | `m07-security-control-evidence-matrix-visual` |
| Category | `security` |
| Module | `module-07` |
| Lesson | 7.2 |
| Lab | lab-07 |
| Learning objective | Security/resilience: Control Evidence Matrix Visual |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-07/mermaid/security/m07-security-control-evidence-matrix-visual.mmd`](module-07/mermaid/security/m07-security-control-evidence-matrix-visual.mmd)
- Draw.io: [`module-07/drawio/security/m07-security-control-evidence-matrix-visual.drawio`](module-07/drawio/security/m07-security-control-evidence-matrix-visual.drawio)
- SVG: [`module-07/svg/security/m07-security-control-evidence-matrix-visual.svg`](module-07/svg/security/m07-security-control-evidence-matrix-visual.svg)
- PNG: [`module-07/png/security/m07-security-control-evidence-matrix-visual.png`](module-07/png/security/m07-security-control-evidence-matrix-visual.png)

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
  Risk["Risk"] --> Control["Control"]
  Control --> Evidence["Evidence"]
  Evidence --> Audit["Audit Ready"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
