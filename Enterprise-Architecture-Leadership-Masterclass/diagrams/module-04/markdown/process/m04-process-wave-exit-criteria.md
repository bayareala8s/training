# Wave Exit Criteria

| Field | Value |
| ----- | ----- |
| ID | `m04-process-wave-exit-criteria` |
| Category | `process` |
| Module | `module-04` |
| Lesson | 4.1 |
| Lab | lab-04 |
| Learning objective | Design target-state: Wave Exit Criteria |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-04/mermaid/process/m04-process-wave-exit-criteria.mmd`](module-04/mermaid/process/m04-process-wave-exit-criteria.mmd)
- Draw.io: [`module-04/drawio/process/m04-process-wave-exit-criteria.drawio`](module-04/drawio/process/m04-process-wave-exit-criteria.drawio)
- SVG: [`module-04/svg/process/m04-process-wave-exit-criteria.svg`](module-04/svg/process/m04-process-wave-exit-criteria.svg)
- PNG: [`module-04/png/process/m04-process-wave-exit-criteria.png`](module-04/png/process/m04-process-wave-exit-criteria.png)

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
  Wave["Wave N"] --> Exit{"Exit Criteria Met?"}
  Exit -->|Yes| Next["Wave N+1"]
  Exit -->|No| Fix["Remediate"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
