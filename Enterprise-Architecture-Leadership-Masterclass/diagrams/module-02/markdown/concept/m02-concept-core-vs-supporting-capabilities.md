# Core vs Supporting Capabilities

| Field | Value |
| ----- | ----- |
| ID | `m02-concept-core-vs-supporting-capabilities` |
| Category | `concept` |
| Module | `module-02` |
| Lesson | 2.1 |
| Lab | — |
| Learning objective | Apply business architecture visual: Core vs Supporting Capabilities |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-02/mermaid/concept/m02-concept-core-vs-supporting-capabilities.mmd`](module-02/mermaid/concept/m02-concept-core-vs-supporting-capabilities.mmd)
- Draw.io: [`module-02/drawio/concept/m02-concept-core-vs-supporting-capabilities.drawio`](module-02/drawio/concept/m02-concept-core-vs-supporting-capabilities.drawio)
- SVG: [`module-02/svg/concept/m02-concept-core-vs-supporting-capabilities.svg`](module-02/svg/concept/m02-concept-core-vs-supporting-capabilities.svg)
- PNG: [`module-02/png/concept/m02-concept-core-vs-supporting-capabilities.png`](module-02/png/concept/m02-concept-core-vs-supporting-capabilities.png)

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
  Core["Core: Payments · Onboarding · Partner"] 
  Supp["Supporting: HR · ITSM · Finance Ops"]
  Comm["Commodity: Email · Collaboration"]
  Core --> Diff["Differentiate"]
  Supp --> Eff["Efficiency"]
  Comm --> Std["Standardize / Buy"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
