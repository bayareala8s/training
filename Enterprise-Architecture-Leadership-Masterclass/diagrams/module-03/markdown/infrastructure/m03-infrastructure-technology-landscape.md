# Technology Landscape

| Field | Value |
| ----- | ----- |
| ID | `m03-infrastructure-technology-landscape` |
| Category | `infrastructure` |
| Module | `module-03` |
| Lesson | 3.4 |
| Lab | lab-03 |
| Learning objective | Assess current estate: Technology Landscape |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-03/mermaid/infrastructure/m03-infrastructure-technology-landscape.mmd`](module-03/mermaid/infrastructure/m03-infrastructure-technology-landscape.mmd)
- Draw.io: [`module-03/drawio/infrastructure/m03-infrastructure-technology-landscape.drawio`](module-03/drawio/infrastructure/m03-infrastructure-technology-landscape.drawio)
- SVG: [`module-03/svg/infrastructure/m03-infrastructure-technology-landscape.svg`](module-03/svg/infrastructure/m03-infrastructure-technology-landscape.svg)
- PNG: [`module-03/png/infrastructure/m03-infrastructure-technology-landscape.png`](module-03/png/infrastructure/m03-infrastructure-technology-landscape.png)

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
  subgraph Stacks["Technology Stacks — NorthStar (fictional)"]
    MF["Mainframe / COBOL"]
    Java["Java / Spring"]
    Dot[".NET"]
    Node["Node / Python"]
    SaaS["SaaS Packaged"]
  end
  MF --> Risk["EOL / Skills Risk"]
  SaaS --> Op["OpEx Concentration"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
