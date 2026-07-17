# Course Diagrams — Enterprise Architecture Leadership Masterclass

First-class visual learning assets for BayLearn.

**Shared standards & reusable library:** [`../diagram-library/`](../diagram-library/)  
**Manifest:** [`diagram-manifest.json`](diagram-manifest.json)  
**Generator:** [`../automation/diagrams/generate_diagram_library.py`](../automation/diagrams/generate_diagram_library.py)

---

## What you get

Every diagram ships in:

| Format | Path pattern |
| ------ | ------------ |
| Mermaid | `…/mermaid/<category>/<id>.mmd` |
| Draw.io | `…/drawio/<category>/<id>.drawio` |
| SVG | `…/svg/<category>/<id>.svg` |
| PNG | `…/png/<category>/<id>.png` |
| Markdown | `…/markdown/<category>/<id>.md` |

Categories: `concept` · `process` · `aws` · `sequence` · `infrastructure` · `dataflow` · `security` · `executive`

---

## Counts (target 150–250; library exceeds)

See `diagram-manifest.json` → `counts.total` and `counts.byModule`.

Minimums met or exceeded for Modules 1–9 and labs; Module 10 + capstone combined ≥ 30.

---

## AWS icons

- Mermaid uses **precise AWS service names** (structure + learning intent)
- Draw.io files are editable masters — open in [diagrams.net](https://app.diagrams.net) and apply **AWS19/AWS23** official stencils for presentation polish
- Never replace AWS icons with generic DB/cloud shapes

See [`../diagram-library/standards/AWS_ICON_STANDARDS.md`](../diagram-library/standards/AWS_ICON_STANDARDS.md).

---

## Regenerate / export SVG

```bash
# Regenerate Mermaid + Draw.io + markdown sources
python3 automation/diagrams/generate_diagram_library.py

# Export ALL diagrams to real SVG
npm install --no-fund --no-audit @mermaid-js/mermaid-cli@11.4.2
python3 automation/diagrams/export_all_svg.py --jobs=4

# Optional PNG @2x
python3 automation/diagrams/export_all_svg.py --jobs=4 --png
```

**Status:** All **320** course diagrams are SVG-exported (`diagrams/**/svg/`). See `qa/diagram-svg-export-qa.md`.

---

## Progressive reveal (PowerPoint)

Draw.io groups are labeled for animation order: `g1_actors` → `g6_observability`.  
Keep major components as separate groups when refining AWS stencil masters.

---

## PlantUML

Sequence-heavy diagrams are also expressed in Mermaid `sequenceDiagram`. Optional PlantUML twins can be added under `…/plantuml/` using the same IDs when instructors prefer PlantUML tooling.
