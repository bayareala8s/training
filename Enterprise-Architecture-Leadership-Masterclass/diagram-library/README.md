# BayLearn Architecture Diagram Library

**Purpose:** First-class, reusable professional diagrams for all BayLearn courses.  
**First consumer:** Enterprise Architecture Leadership Masterclass  
**Visual standard:** AWS Architecture Icons + AWS Well-Architected presentation quality

---

## Principles

1. Diagrams are learning assets, not decorations  
2. Every concept has a professional visual  
3. AWS services always use official AWS Architecture Icons (never generic substitutes)  
4. Source of truth is editable (Mermaid + Draw.io); SVG/PNG are exports  
5. Shared library first — course folders compose and specialize  

---

## Layout

```text
diagram-library/          # Shared across BayLearn courses
├── standards/            # Style guide, taxonomy, AWS icon rules
├── reusable-components/  # Account frames, VPC, trust boundaries, legends
├── templates/            # Starter diagrams by taxonomy
├── business/
├── cloud/
├── aws/
├── networking/
├── security/
├── integration/
├── data/
├── ai/
├── platform-engineering/
├── devops/
├── enterprise-architecture/
└── reference-architectures/

diagrams/                 # Course-specific compositions (this Masterclass)
├── module-01/ … module-10/
├── labs/
├── capstone/
├── executive/
└── diagram-manifest.json
```

---

## Required formats (every diagram)

| Format | Role |
| ------ | ---- |
| Mermaid (`.mmd`) | Source / docs / markdown embed |
| Draw.io (`.drawio`) | Editable with AWS stencils |
| SVG | Presentation / PPT-compatible |
| PNG @2x | Slides, LinkedIn, portals |
| Markdown | Title, LO, description, embed |

Never ship raster-only diagrams.

---

## Start here

1. [`standards/VISUAL_STYLE_GUIDE.md`](standards/VISUAL_STYLE_GUIDE.md)  
2. [`standards/AWS_ICON_STANDARDS.md`](standards/AWS_ICON_STANDARDS.md)  
3. [`standards/TAXONOMY.md`](standards/TAXONOMY.md)  
4. Course manifest: [`../diagrams/diagram-manifest.json`](../diagrams/diagram-manifest.json)  
5. Generator: [`../automation/diagrams/generate_diagram_library.py`](../automation/diagrams/generate_diagram_library.py)

---

## Reuse for future courses

When creating *Terraform for Real Enterprises*, *AI Automation with AWS Bedrock*, etc., import from `diagram-library/` and add course-specific compositions under that course’s `diagrams/` folder — do not fork the visual language.
