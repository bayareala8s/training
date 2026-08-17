# AWS architecture diagrams (student edition)

Detailed **AWS stencil–style** diagrams for every course module. Use these alongside the lecture modules in [`../modules/`](../modules/).

## How to view

| Format | Best for |
|--------|----------|
| **`.md` files** | Read in GitHub, VS Code, or Cursor — Mermaid renders inline |
| **`.drawio` files** | Edit in [diagrams.net](https://app.diagrams.net) with official **AWS Architecture Icons** |
| **PNG / SVG** | Slides, LMS, print — pre-exported in [`export/`](export/README.md) (108 images) |

### Pre-rendered images (PNG & SVG)

All diagrams are exported for offline use:

- **Draw.io stencils:** [`export/png/drawio/`](export/png/drawio/) · [`export/svg/drawio/`](export/svg/drawio/)
- **Mermaid (per diagram in week guides):** [`export/png/mermaid/`](export/png/mermaid/) · [`export/svg/mermaid/`](export/svg/mermaid/)

Regenerate: `./scripts/export_diagram_images.sh` (Docker + Node required).

## Open `.drawio` with AWS stencils

1. Go to [https://app.diagrams.net](https://app.diagrams.net) (or VS Code **Draw.io Integration** extension).
2. **File → Open** → select e.g. `week-01-transfer-edge.drawio`.
3. If icons look like plain boxes: **More Shapes** (bottom left) → enable **AWS / AWS 2024** (or **AWS19**).
4. Export for slides: **File → Export as → PNG or SVG** (300 DPI for print).

## Diagram index

| Week | Module topic | Mermaid guide | Stencil PNG | Mermaid PNGs |
|------|----------------|---------------|-------------|----------------|
| 1 | Transfer Family & landing zone | [week-01.md](week-01.md) | [png](export/png/drawio/week-01-transfer-edge.png) | [folder](export/png/mermaid/) `week-01-diagram-*` |
| 2 | Security, KMS, governance | [week-02.md](week-02.md) | [png](export/png/drawio/week-02-security-governance.png) | `week-02-diagram-*` |
| 3 | Event-driven Lambda | [week-03.md](week-03.md) | [png](export/png/drawio/week-03-event-driven.png) | `week-03-diagram-*` |
| 4 | Step Functions | [week-04.md](week-04.md) | [png](export/png/drawio/week-04-step-functions.png) | `week-04-diagram-*` |
| 5 | Connectors & partners | [week-05.md](week-05.md) | [png](export/png/drawio/week-05-connectors.png) | `week-05-diagram-*` |
| 6 | Self-serve API | [week-06.md](week-06.md) | [png](export/png/drawio/week-06-self-serve-api.png) | `week-06-diagram-*` |
| 7 | Operations | [week-07.md](week-07.md) | [png](export/png/drawio/week-07-observability.png) | `week-07-diagram-*` |
| 8 | Capstone platform | [week-08.md](week-08.md) | [png](export/png/drawio/week-08-capstone-platform.png) | `week-08-diagram-*` |
| 9 | ECS Fargate (stretch) | [week-09.md](week-09.md) | [png](export/png/drawio/week-09-ecs-fargate.png) | `week-09-diagram-*` |

Editable `.drawio` files: same names without `export/png/drawio/` prefix (repo root `docs/diagrams/`).

**Full lab stack (all weeks):** [lab-stack-reference.drawio](lab-stack-reference.drawio)

## Color legend (Mermaid)

Diagrams use colors aligned to the [AWS Architecture Icon](https://aws.amazon.com/architecture/icons/) palette:

| Color | Service category |
|-------|------------------|
| Orange | Compute (Lambda, ECS) |
| Green | Storage (S3) |
| Purple | Transfer / integration |
| Pink | Database (DynamoDB) |
| Red | Security (KMS, Cognito) |
| Blue | Networking (VPC, endpoints) |
| Dark | Management (CloudWatch, Step Functions) |

## Instructor tip

Ask learners to **re-draw** Diagram 1 from memory after each module, then compare to the answer key in the `.md` file.
