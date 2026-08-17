# Capability Heatmap

| Field | Value |
| ----- | ----- |
| ID | `m02-executive-capability-heatmap` |
| Category | `executive` |
| Module | `module-02` |
| Lesson | 2.3 |
| Lab | — |
| Learning objective | Apply business architecture visual: Capability Heatmap |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-02/mermaid/executive/m02-executive-capability-heatmap.mmd`](module-02/mermaid/executive/m02-executive-capability-heatmap.mmd)
- Draw.io: [`module-02/drawio/executive/m02-executive-capability-heatmap.drawio`](module-02/drawio/executive/m02-executive-capability-heatmap.drawio)
- SVG: [`module-02/svg/executive/m02-executive-capability-heatmap.svg`](module-02/svg/executive/m02-executive-capability-heatmap.svg)
- PNG: [`module-02/png/executive/m02-executive-capability-heatmap.png`](module-02/png/executive/m02-executive-capability-heatmap.png)

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
  subgraph Heat["Maturity Heatmap"]
    R1["Onboarding — 2 Fragile"]
    A1["Payments — 3 Adequate"]
    G1["Ledger — 4 Good"]
  end
  R1 --> X["Invest / Migrate"]
  style R1 fill:#FCE8E6,stroke:#D13212
  style A1 fill:#FFF3E0,stroke:#ED7100
  style G1 fill:#F0F7E6,stroke:#1D8102
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
