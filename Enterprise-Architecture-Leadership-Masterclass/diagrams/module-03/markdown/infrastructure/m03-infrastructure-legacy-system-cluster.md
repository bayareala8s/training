# Legacy System Cluster

| Field | Value |
| ----- | ----- |
| ID | `m03-infrastructure-legacy-system-cluster` |
| Category | `infrastructure` |
| Module | `module-03` |
| Lesson | 3.1 |
| Lab | lab-03 |
| Learning objective | Assess current estate: Legacy System Cluster |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-03/mermaid/infrastructure/m03-infrastructure-legacy-system-cluster.mmd`](module-03/mermaid/infrastructure/m03-infrastructure-legacy-system-cluster.mmd)
- Draw.io: [`module-03/drawio/infrastructure/m03-infrastructure-legacy-system-cluster.drawio`](module-03/drawio/infrastructure/m03-infrastructure-legacy-system-cluster.drawio)
- SVG: [`module-03/svg/infrastructure/m03-infrastructure-legacy-system-cluster.svg`](module-03/svg/infrastructure/m03-infrastructure-legacy-system-cluster.svg)
- PNG: [`module-03/png/infrastructure/m03-infrastructure-legacy-system-cluster.png`](module-03/png/infrastructure/m03-infrastructure-legacy-system-cluster.png)

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
  subgraph Acquired["Acquired Estates"]
    MS["Mainstreet Core"]
    EU["Europa Cards Core"]
    Asia["Asia Partner Hub"]
  end
  MS & EU & Asia --> Dup["Duplicate Capabilities"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
