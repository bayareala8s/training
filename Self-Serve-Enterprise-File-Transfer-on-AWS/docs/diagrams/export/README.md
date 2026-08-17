# Exported diagram images (PNG & SVG)

Pre-rendered assets for slides, LMS uploads, and offline study. **108 files** total.

## Layout

| Folder | Source | Count |
|--------|--------|------:|
| [png/drawio/](png/drawio/) | `.drawio` AWS stencil files | 10 |
| [svg/drawio/](svg/drawio/) | `.drawio` AWS stencil files | 10 |
| [png/mermaid/](png/mermaid/) | Mermaid blocks in `week-*.md` | 44 |
| [svg/mermaid/](svg/mermaid/) | Mermaid blocks in `week-*.md` | 44 |

## Naming

- **drawio:** `week-01-transfer-edge.png` (matches `.drawio` basename)
- **mermaid:** `week-04-diagram-02-lab-4-state-machine.png` (week + diagram number + title slug)

## Regenerate

From repo root (requires Docker + Node/npx):

```bash
./scripts/export_diagram_images.sh
```

Uses `fnkr/drawio` for draw.io exports and `@mermaid-js/mermaid-cli` for Mermaid.
