# Trade-off Defense Loop

| Field | Value |
| ----- | ----- |
| ID | `m10-process-trade-off-defense-loop` |
| Category | `process` |
| Module | `module-10` |
| Lesson | 10.4 |
| Lab | lab-10 |
| Learning objective | Capstone leadership: Trade-off Defense Loop |
| AWS icons | _None (non-AWS concept)_ |

## Formats

- Mermaid: [`module-10/mermaid/process/m10-process-trade-off-defense-loop.mmd`](module-10/mermaid/process/m10-process-trade-off-defense-loop.mmd)
- Draw.io: [`module-10/drawio/process/m10-process-trade-off-defense-loop.drawio`](module-10/drawio/process/m10-process-trade-off-defense-loop.drawio)
- SVG: [`module-10/svg/process/m10-process-trade-off-defense-loop.svg`](module-10/svg/process/m10-process-trade-off-defense-loop.svg)
- PNG: [`module-10/png/process/m10-process-trade-off-defense-loop.png`](module-10/png/process/m10-process-trade-off-defense-loop.png)

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
  Claim["Recommendation"] --> Chal["Challenge"]
  Chal --> Alt["Alternatives"]
  Alt --> Cons["Consequences"]
  Cons --> Decide["Decide"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
