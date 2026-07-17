# Dependency-Based Sequencing

| Field | Value |
| ----- | ----- |
| ID | `m04-process-dependency-based-sequencing` |
| Category | `process` |
| Module | `module-04` |
| Lesson | 4.4 |
| Lab | lab-04 |
| Learning objective | Design target-state: Dependency-Based Sequencing |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-04/mermaid/process/m04-process-dependency-based-sequencing.mmd`](module-04/mermaid/process/m04-process-dependency-based-sequencing.mmd)
- Draw.io: [`module-04/drawio/process/m04-process-dependency-based-sequencing.drawio`](module-04/drawio/process/m04-process-dependency-based-sequencing.drawio)
- SVG: [`module-04/svg/process/m04-process-dependency-based-sequencing.svg`](module-04/svg/process/m04-process-dependency-based-sequencing.svg)
- PNG: [`module-04/png/process/m04-process-dependency-based-sequencing.png`](module-04/png/process/m04-process-dependency-based-sequencing.png)

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
  Id["Identity Standard"] --> Apps["App Migrations"]
  Log["Central Logging"] --> Apps
  Hub["Integration Hub"] --> Partner["Partner Onboarding"]
  Hub --> Pay["Payment Events"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
