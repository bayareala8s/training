# Course Architecture Diagrams (Detailed / Instructor-Ready)

Professional **AWS Architecture Icon (aws4)** diagrams designed for teaching — not minimal box-and-arrow sketches.

Each diagram includes:

| Element | Purpose |
|---------|---------|
| **Learning focus banner** | What students should understand from this diagram |
| **Numbered swimlanes / steps** | Clear flow order (①②③ or step badges) |
| **AWS service icons** | Lambda, Bedrock, Step Functions, API Gateway, etc. |
| **Code / schema examples** | JSON payloads, IAM policies, API contracts |
| **Failure paths (red dashed)** | Fallbacks, human review, invalid output |
| **Instructor talking points** | Yellow callouts — what to say in class |
| **Student takeaways** | Purple callouts — what to remember |
| **Legends & checklists** | Governance, logging rules, demo scripts |

## Formats

| Format | Location | Best for |
|--------|----------|----------|
| **Draw.io** | `drawio/*.drawio` | Editing in [diagrams.net](https://app.diagrams.net) with full AWS 2024 stencils |
| **PNG** | `png/*.png` | Slides, LMS, handouts (2× scale) |
| **SVG** | `svg/*.svg` | Web, print, scalable docs |

## Diagram index

| File | Week | What it teaches |
|------|------|-----------------|
| `01-reference` | All | End-to-end production architecture (ingress → orchestration → AI → data/ops) |
| `02-week01` | 1 | Rules vs ML vs LLM decision matrix + enterprise risks |
| `03-week02` | 2 | IAM least privilege, model access, safe logging boundaries |
| `04-week03` | 3 | Structured JSON, validation, confidence gate, hybrid rules+AI |
| `05-week04` | 4 | Step Functions states, retries, idempotency, failure injection |
| `06-week05` | 5 | API platform: endpoints, throttling, errors, cost controls |
| `07-week06` | 6 | Audit pipeline, dashboards, alarms, HITL, governance checklist |
| `08-week07` | 7 | Agent router, tool policy, memory TTL, event chaining |
| `09-week08` | 8 | Four capstone options + minimum bar + demo script |
| `10-iam` | 2,6 | Deploy vs runtime vs API caller identity boundaries |
| `11-labs` | Labs | Live SAM stack mapped to weekly lab resources |

## Regenerate all formats

```bash
cd diagrams
./tools/export_all.sh
```

Requires Python 3.10+ and `cairosvg` for PNG (`pip install cairosvg`).

## Open in Draw.io (recommended for editing)

1. Go to https://app.diagrams.net
2. **File → Open from → Device** → select `drawio/04-week03.drawio`
3. Enable stencil library: **+ More Shapes → AWS → AWS 2024**
4. Edit instructor callouts, add your org name, export from Draw.io if needed

## Instructor tips

- **Week 1**: Start with `02-week01` — establish the "not chatbots" narrative before Bedrock labs.
- **Week 3**: Walk through `04-week03` failure paths before the validation lab — students implement what they see.
- **Week 4**: Use `05-week04` alongside the Step Functions console execution graph.
- **Week 8**: Project `09-week08` during capstone kickoff; students pick one quadrant.

## Licensing

Course materials © BayAreaLa8s. AWS icons per [AWS Architecture Icons guidelines](https://aws.amazon.com/architecture/icons/).
