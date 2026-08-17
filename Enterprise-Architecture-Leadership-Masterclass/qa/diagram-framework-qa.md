# Diagram Framework QA

**Date:** 2026-07-15  
**Status:** Complete (framework + 320 diagram assets)

## Delivered

| Item | Status |
| ---- | ------ |
| Shared `diagram-library/` with standards, taxonomy, AWS icon rules, reusable components | Pass |
| Course `diagrams/` organized by module/lab/capstone | Pass |
| Formats per diagram: Mermaid, Draw.io, SVG, PNG, Markdown | Pass |
| `diagram-manifest.json` with LO, module/lesson/lab mapping, AWS icons | Pass |
| Generator `automation/diagrams/generate_diagram_library.py` | Pass |
| Export helper `automation/diagrams/export_mermaid.sh` | Pass |
| PlantUML sample for sequences | Pass |
| Module minimums (1–9) and Module 10+cap ≥ 30 | Pass |
| Lab sets for AWS labs 5–8 (12 diagrams each) | Pass |

## Counts

**320** diagrams in manifest (exceeds 150–250 target).

## Presentation masters note

Mermaid embeds **cannot** use official AWS SVG icons. Draw.io files are the editable path to apply **AWS19/AWS23** stencils. Run `export_mermaid.sh` for high-fidelity SVG/PNG from Mermaid; refine AWS reference architectures in diagrams.net for LinkedIn/slide masters.

## Fiction

NorthStar labeled fictional on case diagrams / footers.
