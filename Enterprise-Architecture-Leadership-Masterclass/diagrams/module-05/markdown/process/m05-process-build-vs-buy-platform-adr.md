# Build vs Buy Platform ADR

| Field | Value |
| ----- | ----- |
| ID | `m05-process-build-vs-buy-platform-adr` |
| Category | `process` |
| Module | `module-05` |
| Lesson | 5.1 |
| Lab | lab-05 |
| Learning objective | Cloud/platform strategy: Build vs Buy Platform ADR |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-05/mermaid/process/m05-process-build-vs-buy-platform-adr.mmd`](module-05/mermaid/process/m05-process-build-vs-buy-platform-adr.mmd)
- Draw.io: [`module-05/drawio/process/m05-process-build-vs-buy-platform-adr.drawio`](module-05/drawio/process/m05-process-build-vs-buy-platform-adr.drawio)
- SVG: [`module-05/svg/process/m05-process-build-vs-buy-platform-adr.svg`](module-05/svg/process/m05-process-build-vs-buy-platform-adr.svg)
- PNG: [`module-05/png/process/m05-process-build-vs-buy-platform-adr.png`](module-05/png/process/m05-process-build-vs-buy-platform-adr.png)

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
  Need["Platform Need"] --> Opt["Build · Buy · Reuse"]
  Opt --> ADR["ADR"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
