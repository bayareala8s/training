# AWS architecture diagrams (student edition)

Detailed **AWS stencil–style** diagrams for every course module. Use these alongside the lecture modules in [`../modules/`](../modules/).

## How to view

| Format | Best for |
|--------|----------|
| **`.md` files** | Read in GitHub, VS Code, or Cursor — Mermaid renders inline |
| **`.drawio` files** | Edit in [diagrams.net](https://app.diagrams.net) with official **AWS Architecture Icons** |

## Open `.drawio` with AWS stencils

1. Go to [https://app.diagrams.net](https://app.diagrams.net) (or VS Code **Draw.io Integration** extension).
2. **File → Open** → select e.g. `week-01-transfer-edge.drawio`.
3. If icons look like plain boxes: **More Shapes** (bottom left) → enable **AWS / AWS 2024** (or **AWS19**).
4. Export for slides: **File → Export as → PNG or SVG** (300 DPI for print).

## Diagram index

| Week | Module topic | Mermaid guide | Editable stencil |
|------|----------------|---------------|------------------|
| 1 | Transfer Family & landing zone | [week-01.md](week-01.md) | [week-01-transfer-edge.drawio](week-01-transfer-edge.drawio) |
| 2 | Security, KMS, governance | [week-02.md](week-02.md) | [week-02-security-governance.drawio](week-02-security-governance.drawio) |
| 3 | Event-driven Lambda | [week-03.md](week-03.md) | [week-03-event-driven.drawio](week-03-event-driven.drawio) |
| 4 | Step Functions orchestration | [week-04.md](week-04.md) | [week-04-step-functions.drawio](week-04-step-functions.drawio) |
| 5 | Connectors & partners | [week-05.md](week-05.md) | [week-05-connectors.drawio](week-05-connectors.drawio) |
| 6 | Self-serve API | [week-06.md](week-06.md) | [week-06-self-serve-api.drawio](week-06-self-serve-api.drawio) |
| 7 | Operations & observability | [week-07.md](week-07.md) | [week-07-observability.drawio](week-07-observability.drawio) |
| 8 | Capstone (full platform) | [week-08.md](week-08.md) | [week-08-capstone-platform.drawio](week-08-capstone-platform.drawio) |
| 9 | ECS Fargate (stretch) | [week-09.md](week-09.md) | [week-09-ecs-fargate.drawio](week-09-ecs-fargate.drawio) |

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
