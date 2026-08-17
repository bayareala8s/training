# Developer Platform Layers

| Field | Value |
| ----- | ----- |
| ID | `m05-concept-developer-platform-layers` |
| Category | `concept` |
| Module | `module-05` |
| Lesson | 5.1 |
| Lab | lab-05 |
| Learning objective | Cloud/platform strategy: Developer Platform Layers |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-05/mermaid/concept/m05-concept-developer-platform-layers.mmd`](module-05/mermaid/concept/m05-concept-developer-platform-layers.mmd)
- Draw.io: [`module-05/drawio/concept/m05-concept-developer-platform-layers.drawio`](module-05/drawio/concept/m05-concept-developer-platform-layers.drawio)
- SVG: [`module-05/svg/concept/m05-concept-developer-platform-layers.svg`](module-05/svg/concept/m05-concept-developer-platform-layers.svg)
- PNG: [`module-05/png/concept/m05-concept-developer-platform-layers.png`](module-05/png/concept/m05-concept-developer-platform-layers.png)

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
  UX["Developer UX"] --> Paths["Golden Paths"]
  Paths --> Comp["Platform Capabilities"]
  Comp --> Cloud["Cloud Foundations"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
