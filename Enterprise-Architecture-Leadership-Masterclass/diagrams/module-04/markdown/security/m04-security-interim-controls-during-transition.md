# Interim Controls During Transition

| Field | Value |
| ----- | ----- |
| ID | `m04-security-interim-controls-during-transition` |
| Category | `security` |
| Module | `module-04` |
| Lesson | 4.1 |
| Lab | lab-04 |
| Learning objective | Design target-state: Interim Controls During Transition |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-04/mermaid/security/m04-security-interim-controls-during-transition.mmd`](module-04/mermaid/security/m04-security-interim-controls-during-transition.mmd)
- Draw.io: [`module-04/drawio/security/m04-security-interim-controls-during-transition.drawio`](module-04/drawio/security/m04-security-interim-controls-during-transition.drawio)
- SVG: [`module-04/svg/security/m04-security-interim-controls-during-transition.svg`](module-04/svg/security/m04-security-interim-controls-during-transition.svg)
- PNG: [`module-04/png/security/m04-security-interim-controls-during-transition.png`](module-04/png/security/m04-security-interim-controls-during-transition.png)

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
  Dual["Dual-run Period"] --> Ctrl["Compensating Controls"]
  Ctrl --> Mon["Extra Monitoring"]
  Ctrl --> Exc["Time-boxed Exceptions"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
