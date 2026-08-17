# Duplicate Capability Detection

| Field | Value |
| ----- | ----- |
| ID | `m03-concept-duplicate-capability-detection` |
| Category | `concept` |
| Module | `module-03` |
| Lesson | 3.3 |
| Lab | lab-03 |
| Learning objective | Assess current estate: Duplicate Capability Detection |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-03/mermaid/concept/m03-concept-duplicate-capability-detection.mmd`](module-03/mermaid/concept/m03-concept-duplicate-capability-detection.mmd)
- Draw.io: [`module-03/drawio/concept/m03-concept-duplicate-capability-detection.drawio`](module-03/drawio/concept/m03-concept-duplicate-capability-detection.drawio)
- SVG: [`module-03/svg/concept/m03-concept-duplicate-capability-detection.svg`](module-03/svg/concept/m03-concept-duplicate-capability-detection.svg)
- PNG: [`module-03/png/concept/m03-concept-duplicate-capability-detection.png`](module-03/png/concept/m03-concept-duplicate-capability-detection.png)

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
  Cap["Capability: File Transfer"] --> S1["SFTP Hub East"]
  Cap --> S2["SFTP Hub West"]
  Cap --> S3["PartnerFile Dropzone"]
  S1 & S2 & S3 --> Consol["Consolidate"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
