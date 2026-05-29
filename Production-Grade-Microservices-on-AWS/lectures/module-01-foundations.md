# Module 1 — Microservices Foundations

**Production-Grade Microservices on AWS · BayAreaLa8s**

| | |
|---|---|
| **Duration** | 90 minutes lecture + 4 hours lab |
| **Week** | 1 of 10 |
| **Prerequisites** | Programming fundamentals, basic REST APIs, Git |

---

## Learning Objectives

By the end of this session, students will be able to:

1. **Compare** monolithic and microservices architectures using deployment, data, team, and operational dimensions.
2. **Define** bounded contexts, ubiquitous language, and context maps in Domain-Driven Design (DDD).
3. **Assign** service ownership using the “you build it, you run it” model.
4. **Identify** five common anti-patterns that cause distributed monoliths or production failures.
5. **Decompose** a sample e-commerce domain into four course-aligned services: Identity, Catalog, Orders, and Notifications.

---

## Session Agenda

| Segment | Time | Topic |
|---------|------|--------|
| Opening & framing | 10 min | Why production microservices are an organizational choice |
| Monolith vs microservices | 25 min | Trade-offs, when to split, when not to |
| Domain-Driven Design | 25 min | Language, boundaries, context maps |
| Service ownership | 15 min | Teams, on-call, API contracts |
| Anti-patterns & pitfalls | 10 min | What breaks in real enterprises |
| Wrap-up & lab preview | 5 min | Assignment 1, Lab 01 |

**Diagrams for this module:** [02-monolith-vs-microservices](../docs/diagrams/02-monolith-vs-microservices.md) · [03-bounded-contexts](../docs/diagrams/03-bounded-contexts-context-map.md) · [04-c4-system-context](../docs/diagrams/04-c4-system-context.md)

---

## 1. Opening: Production Is the Product (10 minutes)

### Instructor script

> “Who has deployed code to production? Who has been on-call when something broke at 2 a.m.?”

Microservices are often taught as a **technology pattern** (small services + HTTP). In enterprise practice, they are primarily an **organizational and operational** pattern: independent teams ship independent deployable units with clear ownership.

**Key message:** If you cannot operate many services (observability, deployments, incident response), microservices will increase pain—not reduce it.

### What “production-grade” means in this course

| Capability | Student outcome by Week 10 |
|------------|----------------------------|
| Design | Bounded contexts, API contracts, event schemas |
| Build | Four services (Python reference), Docker images |
| Deploy | ECS Fargate, ALB, Terraform, ECR |
| Secure | JWT, IAM task roles, private subnets |
| Operate | CloudWatch, CI/CD, cost start/stop |

### Course platform preview

Students will build an e-commerce-style platform:

| Service | Port (local) | Responsibility |
|---------|--------------|----------------|
| User | 8001 | Registration, login, JWT |
| Product | 8002 | Catalog, SKU, stock |
| Order | 8003 | Checkout, calls Product, publishes events |
| Notification | 8004 | Consumes `OrderPlaced`, logs / simulates email |

See [01-platform-overview](../docs/diagrams/01-platform-overview.md) (Mermaid + PNG in `docs/diagrams/png/`).

---

## 2. Monolith vs Microservices (25 minutes)

### 2.1 Definitions

**Monolith:** One deployable application containing most business capabilities. Often one codebase and frequently one shared database.

**Microservices:** Suite of small services, each aligned to a business capability, independently deployable, each owning its data and exposing contracts (APIs/events) to others.

### 2.2 Comparison matrix

| Dimension | Monolith | Microservices |
|-----------|----------|---------------|
| **Deploy unit** | Single artifact | Many artifacts (per service) |
| **Data** | Often one shared DB | Database-per-service (ideal) |
| **Team scaling** | Everyone touches same repo | Teams align to service boundaries |
| **Failure blast radius** | Whole app can fail | Isolated if boundaries are real |
| **Consistency** | ACID in one DB is easy | Cross-service = eventual consistency |
| **Complexity** | Lower initially | Higher always (network, ops, debugging) |
| **Time to first feature** | Fast for small teams | Slower until platform maturity exists |

### 2.3 Why large companies adopted services

**Conceptual drivers (Amazon / Netflix narrative):**

- **Organizational scale:** Hundreds of teams cannot merge to one release train daily.
- **Independent velocity:** Catalog team ships without waiting for Payments.
- **Technology diversity:** Different services can use different stacks (with governance).
- **Resilience goals:** Isolate failures—*if* boundaries and fallbacks are well designed.

**Important nuance:** Netflix did not start with 700 microservices. They evolved as operational maturity (automation, observability, culture) caught up.

### 2.4 When microservices are the wrong choice

Avoid splitting when:

- Team is **small** (< ~8 engineers) and domain is still **unclear**
- No **CI/CD**, **monitoring**, or **on-call** culture exists yet
- Problem is **premature optimization** for scale you do not have
- You need **strong cross-entity transactions** everywhere (consider monolith or modular monolith first)

**Modular monolith (mention):** Single deployable with clear internal modules and boundaries—often the best first step before network distribution.

### 2.5 Distributed monolith

A system that *looks* like microservices but behaves like a monolith:

- Synchronous chains of 5+ HTTP calls per user request
- Shared database across “services”
- Must deploy all services together for any change
- No clear ownership

**Teaching point:** Count **independent deploys per week per team**, not **number of repos**.

### Class discussion (3 minutes)

> “A startup with five engineers wants microservices for their MVP. What do you advise?”

*Expected answers:* Start monolith or modular monolith; invest in CI and tests; split when team or domain pain justifies operational cost.

---

## 3. Domain-Driven Design for Service Boundaries (25 minutes)

### 3.1 Ubiquitous language

The **same vocabulary** must be used by product, engineering, and support.

| Context | “Order” might mean |
|---------|-------------------|
| E-commerce | Cart checkout, payment capture, shipment |
| Banking | Wire transfer instruction |
| SaaS billing | Subscription invoice line |

If one service mixes these meanings, the model becomes unmaintainable.

**Exercise (5 minutes, pairs):** List three terms that differ between e-commerce Catalog vs Orders contexts (e.g. *SKU*, *line item*, *placed*).

### 3.2 Bounded context

A **bounded context** is the boundary within which a domain model is consistent.

**Course contexts:**

| Context | Core concepts | Service |
|---------|---------------|---------|
| **Identity** | User, credentials, JWT, session | User Service |
| **Catalog** | Product, SKU, price, stock view | Product Service |
| **Orders** | Order, line item, total, checkout | Order Service |
| **Notifications** | OrderPlaced, confirmation, delivery log | Notification Service |

### 3.3 Context map (relationships)

Show [03-bounded-contexts-context-map](../docs/diagrams/03-bounded-contexts-context-map.md).

| Relationship | Example in course | Integration style |
|--------------|-------------------|-------------------|
| **Customer–Supplier** | Orders → Catalog | Orders calls Product HTTP API |
| **Published language** | Orders → Notifications | `OrderPlaced` event schema |
| **Conformist** | Notifications accepts Orders’ event shape | Shared contract file |
| **Anti-corruption layer** | (extension) | Translate external vendor API |

Orders must **not** query Product’s database tables directly.

### 3.4 Sizing services: capability vs nanoservice

**Good size:** One **business capability** per service (e.g. “take and record orders”).

**Too small:** “EmailValidatorService” with one endpoint—operations overhead dominates.

**Too large:** “CommerceService” owning catalog + orders + payments—back to monolith.

### 3.5 C4 Model — System Context (Level 1)

Introduce [04-c4-system-context](../docs/diagrams/04-c4-system-context.md):

- **Person:** Customer, Admin, Operator
- **System:** Microservices Platform (black box at this level)
- **External:** Email provider, future IdP

Container and component diagrams come in Module 2.

---

## 4. Service Ownership (15 minutes)

### 4.1 “You build it, you run it”

Each team owns:

- **Roadmap** for their capability
- **SLAs/SLOs** (introduced formally in Module 8)
- **On-call** rotation for their service
- **Runbooks** for incidents

### 4.2 API as contract

Other teams depend on **published contracts**, not internal implementation:

- OpenAPI for HTTP (`contracts/openapi/`)
- JSON Schema for events (`contracts/events/order-placed.json`)

**Breaking changes** require versioning and deprecation policy (Module 2).

### 4.3 Conway’s Law

> Organizations design systems that mirror their communication structure.

If teams are split by layer (UI team, DB team), you get **layered monoliths**. Align teams to **business capabilities** for successful microservices.

### 4.4 Platform team (optional mention)

Many enterprises add a **platform engineering** team: ECS clusters, Terraform modules, golden CI templates—so product teams focus on business logic.

---

## 5. Common Pitfalls (10 minutes)

| # | Pitfall | Symptom | Course mitigation |
|---|---------|---------|-------------------|
| 1 | **Shared database** | Hidden joins across services | DB-per-service; Order calls Product API |
| 2 | **Chatty sync** | Latency, cascading failures | Events for notifications; timeouts later |
| 3 | **No observability** | Cannot debug production | CloudWatch Module 8 |
| 4 | **Premature split** | 12 tiny services, no owners | Capstone min. 3 services, clear contexts |
| 5 | **Ignoring eventual consistency** | “Why is email late?” | Events, idempotency Module 5 |

### Shared database anti-pattern (deep dive)

```
❌ Order Service → SELECT * FROM products WHERE id = ?
✅ Order Service → GET /products/:id  (Product Service owns data)
```

**Why it fails:** Schema coupling, breaking changes, no clear owner, scaling limits.

---

## 6. Wrap-Up (5 minutes)

### Summary

- Microservices trade **operational complexity** for **organizational scale** and **independent delivery**.
- **DDD** gives language and boundaries; **context maps** document integration.
- **Ownership** and **contracts** matter as much as code.
- This course’s four-service platform is intentionally sized for learning production practices.

### Lab 01 — Architecture decomposition

- **Lab guide:** [`labs/module-01/README.md`](../labs/module-01/README.md)
- **Deliverables:** Service decomposition doc + context map (templates in lab)
- **Verify:** `./labs/module-01/verify.sh` (checks repo structure and doc presence)

### Assignment 1

See [`assignments/module-01.md`](../assignments/module-01.md).

### Pre-read for Week 2

- Skim [`contracts/openapi/user-service.yaml`](../contracts/openapi/user-service.yaml)
- Review [06-api-contracts](../docs/diagrams/06-api-contracts.md)

---

## Discussion Questions (for async forum or review)

1. Why is a shared database between Order and Product services an anti-pattern even if it “works” in development?
2. How would you decompose a ride-sharing app differently for 5 engineers vs 500 engineers?
3. Give an example of **ubiquitous language** conflict between “customer” in Identity vs Billing contexts.
4. What is a **distributed monolith**? How would you detect one in production metrics?

---

## Instructor Reference

| Resource | Location |
|----------|----------|
| Facilitation notes | [`instructor/module-01.md`](../instructor/module-01.md) |
| Weekly diagram plan | [`docs/diagrams/WEEKLY-DIAGRAM-SCHEDULE.md`](../docs/diagrams/WEEKLY-DIAGRAM-SCHEDULE.md) |
| Student handbook | [`docs/STUDENT_HANDBOOK.md`](../docs/STUDENT_HANDBOOK.md) |

---

*BayAreaLa8s · Production-Grade Microservices on AWS*
