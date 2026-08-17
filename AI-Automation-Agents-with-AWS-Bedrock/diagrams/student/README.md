# Student Diagrams

Action-oriented visuals for labs, assignments, and capstone prep. Each diagram answers one student question: *What happens on a single request?* *What do I log?* *What do I do next?*

## Formats

| Format | Location | Use in LMS |
|--------|----------|------------|
| PNG | `png/*.png` | Embed in Canvas/Moodle/week pages |
| SVG | `svg/*.svg` | Scalable web / print |
| Draw.io | `drawio/*.drawio` | Customize for your cohort |

## Index

### Sequence flows (time → left to right)

| Diagram | Week | Link |
|---------|------|------|
| Request sequence | 3 | [PNG](png/seq-week03.png) · [SVG](svg/seq-week03.svg) |
| Step Functions timeline | 4 | [PNG](png/seq-week04.png) · [SVG](svg/seq-week04.svg) |
| API request flow | 5 | [PNG](png/seq-week05.png) · [SVG](svg/seq-week05.svg) |
| Agent turn | 7 | [PNG](png/seq-week07.png) · [SVG](svg/seq-week07.svg) |

### Cheat sheets (print or pin during labs)

| Diagram | Week | Link |
|---------|------|------|
| Schema + confidence gate | 3 | [PNG](png/cheat-week03.png) |
| Step Functions states | 4 | [PNG](png/cheat-week04.png) |
| Logging & audit | 6 | [PNG](png/cheat-week06.png) |
| Capstone checklist | 8 | [PNG](png/cheat-week08.png) |

### Lab guides

| Diagram | Link |
|---------|------|
| Deploy cycle (`cycle.sh`) | [PNG](png/lab-deploy-cycle.png) |
| Console checkpoints | [PNG](png/lab-console-checkpoints.png) |

### Anti-pattern vs production

| Diagram | Week | Link |
|---------|------|------|
| Raw LLM vs validated JSON | 3 | [PNG](png/pattern-week03.png) |
| Log everything vs audit | 6 | [PNG](png/pattern-week06.png) |
| Unlimited agent vs policy | 7 | [PNG](png/pattern-week07.png) |

## Regenerate

From repo root:

```bash
cd diagrams && ./tools/export_all.sh
```
