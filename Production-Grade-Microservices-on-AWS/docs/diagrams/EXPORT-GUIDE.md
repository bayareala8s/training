# Exporting Diagrams for Slides & Handouts

Pre-rendered assets are in **`png/`** and **`svg/`** (one file per Mermaid block in each numbered diagram). Regenerate after editing source `.md` files.

## Regenerate all exports (recommended)

From the repo root (requires **Node.js** and **npx**):

```bash
make diagrams
# or
./scripts/export-diagrams.sh
```

This uses [@mermaid-js/mermaid-cli](https://github.com/mermaid-js/mermaid-cli) with `mermaid-config.json` (neutral theme, 1920px-wide PNGs, transparent background).

**Naming:** `01-platform-overview.png` for a single diagram per file; `09-event-driven-flow-1.png`, `-2.png`, … when a file has multiple blocks.

## Manual export (no CLI)

1. Open [https://mermaid.live](https://mermaid.live)
2. Copy the contents of a ` ```mermaid ` code block from any diagram file
3. Paste into the editor
4. **Actions → Export PNG** or **SVG** (use 2x scale for slides)

## VS Code / Cursor

1. Install extension: **Markdown Preview Mermaid Support**
2. Open diagram `.md` file → `Cmd+Shift+V` (Preview)
3. Use committed `png/` / `svg/` for slides, or Mermaid Live for custom sizing

## AWS Architecture Icons (detailed stencils)

Pre-built **AWS stencil** diagrams (VPC, ECS, ALB, EventBridge, IAM, CI/CD):

- **PNG / SVG:** [`aws-stencils/png/`](aws-stencils/png/) and [`aws-stencils/svg/`](aws-stencils/svg/)
- **Editable draw.io:** [`aws-stencils/drawio/`](aws-stencils/drawio/) — open in [diagrams.net](https://app.diagrams.net)
- **Regenerate:** `make diagrams` (needs Graphviz + `diagrams` Python package — see [aws-stencils/README.md](aws-stencils/README.md))

## Draw.io / Lucidchart (custom edits)

1. Start from `aws-stencils/drawio/*.drawio` **or** import Mermaid SVG from `svg/`
2. Use the **AWS 2024** shape library in diagrams.net
3. Align with `10-aws-deployment-architecture.md` and `infrastructure/terraform/`

## Suggested slide dimensions

| Use | Asset |
|-----|--------|
| PowerPoint / Keynote | `png/*.png` (1920px wide) |
| Workbook / PDF | `svg/*.svg` (vector) |
| LMS thumbnail | Re-export with `-w 1200` via mmdc if needed |

## Branding (BayAreaLa8s)

Add footer on slides: *Production-Grade Microservices on AWS — BayAreaLa8s*
