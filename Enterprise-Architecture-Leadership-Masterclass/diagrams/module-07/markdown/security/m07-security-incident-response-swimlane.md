# Incident Response Swimlane

| Field | Value |
| ----- | ----- |
| ID | `m07-security-incident-response-swimlane` |
| Category | `security` |
| Module | `module-07` |
| Lesson | 7.4 |
| Lab | lab-07 |
| Learning objective | Security/resilience: Incident Response Swimlane |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-07/mermaid/security/m07-security-incident-response-swimlane.mmd`](module-07/mermaid/security/m07-security-incident-response-swimlane.mmd)
- Draw.io: [`module-07/drawio/security/m07-security-incident-response-swimlane.drawio`](module-07/drawio/security/m07-security-incident-response-swimlane.drawio)
- SVG: [`module-07/svg/security/m07-security-incident-response-swimlane.svg`](module-07/svg/security/m07-security-incident-response-swimlane.svg)
- PNG: [`module-07/png/security/m07-security-incident-response-swimlane.png`](module-07/png/security/m07-security-incident-response-swimlane.png)

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
  Sec["Security"] --> Triage
  Plat["Platform"] --> Triage
  Triage --> Mitigate --> Recover
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
