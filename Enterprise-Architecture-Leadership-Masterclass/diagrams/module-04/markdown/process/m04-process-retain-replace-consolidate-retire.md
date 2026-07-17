# Retain Replace Consolidate Retire

| Field | Value |
| ----- | ----- |
| ID | `m04-process-retain-replace-consolidate-retire` |
| Category | `process` |
| Module | `module-04` |
| Lesson | 4.3 |
| Lab | lab-04 |
| Learning objective | Design target-state: Retain Replace Consolidate Retire |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-04/mermaid/process/m04-process-retain-replace-consolidate-retire.mmd`](module-04/mermaid/process/m04-process-retain-replace-consolidate-retire.mmd)
- Draw.io: [`module-04/drawio/process/m04-process-retain-replace-consolidate-retire.drawio`](module-04/drawio/process/m04-process-retain-replace-consolidate-retire.drawio)
- SVG: [`module-04/svg/process/m04-process-retain-replace-consolidate-retire.svg`](module-04/svg/process/m04-process-retain-replace-consolidate-retire.svg)
- PNG: [`module-04/png/process/m04-process-retain-replace-consolidate-retire.png`](module-04/png/process/m04-process-retain-replace-consolidate-retire.png)

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
  Port["Portfolio"] --> R1["Retain"]
  Port --> R2["Replace"]
  Port --> R3["Consolidate"]
  Port --> R4["Retire"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
