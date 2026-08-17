# Capstone Artifact Dependency Graph

| Field | Value |
| ----- | ----- |
| ID | `m10-concept-capstone-artifact-dependency-graph` |
| Category | `concept` |
| Module | `module-10` |
| Lesson | 10.1 |
| Lab | lab-10 |
| Learning objective | Capstone visual: Capstone Artifact Dependency Graph |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-10/mermaid/concept/m10-concept-capstone-artifact-dependency-graph.mmd`](module-10/mermaid/concept/m10-concept-capstone-artifact-dependency-graph.mmd)
- Draw.io: [`module-10/drawio/concept/m10-concept-capstone-artifact-dependency-graph.drawio`](module-10/drawio/concept/m10-concept-capstone-artifact-dependency-graph.drawio)
- SVG: [`module-10/svg/concept/m10-concept-capstone-artifact-dependency-graph.svg`](module-10/svg/concept/m10-concept-capstone-artifact-dependency-graph.svg)
- PNG: [`module-10/png/concept/m10-concept-capstone-artifact-dependency-graph.png`](module-10/png/concept/m10-concept-capstone-artifact-dependency-graph.png)

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
  Principles --> Capability
  Capability --> Current
  Current --> Target
  Target --> Roadmap
  Roadmap --> Memo
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
