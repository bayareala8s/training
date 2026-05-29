# Course Diagrams — Production-Grade Microservices on AWS

Professional architecture diagrams for instructors and students. Source diagrams use **Mermaid** in numbered `.md` files; **PNG** and **SVG** exports are ready for slides and handouts.

**AWS stencil diagrams** (official AWS Architecture Icons, VPC/ECS detail): see **[aws-stencils/](aws-stencils/)** — PNG, SVG, and editable draw.io sources.

## How to view

| Method | Steps |
|--------|--------|
| **Slides / PDF** | Use files in [`png/`](png/) or [`svg/`](svg/) |
| **VS Code / Cursor** | Open any `.md` file → Markdown Preview |
| **GitHub** | Push repo → Mermaid in `.md` renders automatically |
| **Regenerate exports** | `make diagrams` from repo root (see [EXPORT-GUIDE.md](EXPORT-GUIDE.md)) |

## Diagram index

**46** Mermaid blocks exported as matching **PNG** + **SVG** files (e.g. `png/09-event-driven-flow-1.png`). Files with multiple diagrams use `-1`, `-2`, … suffixes.

| # | Diagram | Source | PNG / SVG (first slide) | Module |
|---|---------|--------|-------------------------|--------|
| 1 | Platform overview | [01](01-platform-overview.md) | [png](png/01-platform-overview.png) · [svg](svg/01-platform-overview.svg) | Intro |
| 2 | Monolith vs microservices | [02](02-monolith-vs-microservices.md) | [png](png/02-monolith-vs-microservices-1.png) · [svg](svg/02-monolith-vs-microservices-1.svg) | 1 |
| 3 | Bounded contexts | [03](03-bounded-contexts-context-map.md) | [png](png/03-bounded-contexts-context-map-1.png) · [svg](svg/03-bounded-contexts-context-map-1.svg) | 1 |
| 4 | C4 — System context | [04](04-c4-system-context.md) | [png](png/04-c4-system-context.png) · [svg](svg/04-c4-system-context.svg) | 1 |
| 5 | C4 — Containers | [05](05-c4-container-diagram.md) | [png](png/05-c4-container-diagram.png) · [svg](svg/05-c4-container-diagram.svg) | 2 |
| 6 | API contracts | [06](06-api-contracts.md) | [png](png/06-api-contracts-1.png) · [svg](svg/06-api-contracts-1.svg) | 2 |
| 7 | Docker Compose local | [07](07-local-docker-compose.md) | [png](png/07-local-docker-compose-1.png) · [svg](svg/07-local-docker-compose-1.svg) | 3 |
| 8 | Place order sequence | [08](08-sequence-place-order.md) | [png](png/08-sequence-place-order-1.png) · [svg](svg/08-sequence-place-order-1.svg) | 2, 5 |
| 9 | Event-driven flow | [09](09-event-driven-flow.md) | [png](png/09-event-driven-flow-1.png) · [svg](svg/09-event-driven-flow-1.svg) | 5 |
| 10 | AWS deployment | [10](10-aws-deployment-architecture.md) | [png](png/10-aws-deployment-architecture-1.png) · [svg](svg/10-aws-deployment-architecture-1.svg) | 4 |
| 11 | Data ownership | [11](11-data-ownership.md) | [png](png/11-data-ownership-1.png) · [svg](svg/11-data-ownership-1.svg) | 6 |
| 12 | Saga & consistency | [12](12-saga-consistency.md) | [png](png/12-saga-consistency-1.png) · [svg](svg/12-saga-consistency-1.svg) | 6 |
| 13 | Security | [13](13-security-architecture.md) | [png](png/13-security-architecture-1.png) · [svg](svg/13-security-architecture-1.svg) | 7 |
| 14 | Observability | [14](14-observability.md) | [png](png/14-observability-1.png) · [svg](svg/14-observability-1.svg) | 8 |
| 15 | CI/CD pipeline | [15](15-cicd-pipeline.md) | [png](png/15-cicd-pipeline-1.png) · [svg](svg/15-cicd-pipeline-1.svg) | 9 |
| 16 | Capstone reference | [16](16-capstone-ecommerce.md) | [png](png/16-capstone-ecommerce-1.png) · [svg](svg/16-capstone-ecommerce-1.svg) | 10 |
| 17 | AWS cost lifecycle | [17](17-aws-cost-lifecycle.md) | [png](png/17-aws-cost-lifecycle-1.png) · [svg](svg/17-aws-cost-lifecycle-1.svg) | Instructor |

## Export for print / slides

| Format | Location |
|--------|----------|
| PNG (1920px wide) | [`docs/diagrams/png/`](png/) |
| SVG (vector) | [`docs/diagrams/svg/`](svg/) |

See [EXPORT-GUIDE.md](EXPORT-GUIDE.md) to regenerate after edits or customize export size.

## Instructor tip

Show diagrams in this order for a new cohort:

1. Monolith vs microservices → Context map → C4 context → C4 containers  
2. Sequence (place order) → Event flow  
3. Docker local → AWS deployment  
4. Security → Observability → CI/CD
