# Lab 1 — Service Decomposition & Bounded Contexts

**Duration:** 4 hours | **Module 1**

## Objectives

- Compare monolith vs microservices trade-offs
- Define bounded contexts for the course e-commerce domain
- Produce a context map and decomposition document

## Prerequisites

- None (no coding this week)

## Part A — Monolith Analysis (60 min)

Review the fictional **ShopMonolith** described below:

| Capability | Tables / Modules |
|------------|------------------|
| Users | `users`, `sessions` |
| Catalog | `products`, `categories` |
| Orders | `orders`, `order_items` |
| Notifications | email templates, send log |

**Discuss:** What changes most often? What scales independently? What fails independently?

## Part B — Define Bounded Contexts (90 min)

Create four contexts aligned with this course:

1. **Identity** — registration, login
2. **Catalog** — products, pricing, stock
3. **Orders** — checkout, order state
4. **Notifications** — email/SMS reactions to events

For each context document:

- Ubiquitous language (5–10 terms)
- Owned data (entities)
- Public API (operations other contexts may call)
- Events published/consumed

## Part C — Context Map (60 min)

Draw a context map showing:

- Customer-Supplier relationships
- Events vs synchronous calls
- Anti-corruption layers where needed

Use draw.io, Miro, or `templates/context-map.drawio` (create your own).

## Part D — Decomposition Document (30 min)

Submit a 2–3 page document covering:

1. Problem statement
2. Service list with responsibilities
3. Data ownership rules (database-per-service)
4. Top 3 pitfalls you will avoid

## Verify your work

```bash
./labs/module-01/verify.sh
```

## Deliverables

- [ ] `docs/your-name/context-map.png` (or PDF)
- [ ] `docs/your-name/service-decomposition.md`

## Instructor Notes

See `instructor/module-01.md`. Common mistake: one “shared” database across all services.
