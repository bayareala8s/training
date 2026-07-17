# Failure Injection Learning

| Field | Value |
| ----- | ----- |
| ID | `m07-security-failure-injection-learning` |
| Category | `security` |
| Module | `module-07` |
| Lesson | 7.3 |
| Lab | lab-07 |
| Learning objective | Security/resilience: Failure Injection Learning |
| AWS icons | Amazon CloudWatch |

## Formats

- Mermaid: [`module-07/mermaid/security/m07-security-failure-injection-learning.mmd`](module-07/mermaid/security/m07-security-failure-injection-learning.mmd)
- Draw.io: [`module-07/drawio/security/m07-security-failure-injection-learning.drawio`](module-07/drawio/security/m07-security-failure-injection-learning.drawio)
- SVG: [`module-07/svg/security/m07-security-failure-injection-learning.svg`](module-07/svg/security/m07-security-failure-injection-learning.svg)
- PNG: [`module-07/png/security/m07-security-failure-injection-learning.png`](module-07/png/security/m07-security-failure-injection-learning.png)

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
  Fail["Inject Failure"] --> Observe["Observe Alarms"]
  Observe --> Learn["Improve Design"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
