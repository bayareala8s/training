# Module 1 Lecture — Microservices Foundations

**Duration:** 90 minutes

## Learning Objectives

Students will explain when microservices help vs hurt, define bounded contexts, and assign service ownership.

---

## 1. Opening (10 min)

**Poll:** Who has deployed to production? Who has been on-call?

**Key message:** Production microservices are an **organizational** and **operational** choice—not only a technology choice.

---

## 2. Monolith vs Microservices (25 min)

| Dimension | Monolith | Microservices |
|-----------|----------|---------------|
| Deploy unit | One | Many |
| Data | Often one DB | DB per service |
| Team scaling | Harder | Align to services |
| Failure blast radius | Large | Smaller (if bounded) |
| Complexity | Lower initially | Higher always |

**Netflix / Amazon anecdote (conceptual):** Scale drove service boundaries—not fashion.

**When NOT to split:** Small team, unclear domain, no ops maturity.

---

## 3. Domain-Driven Design (25 min)

- **Ubiquitous language** — same words in code and business
- **Bounded context** — explicit model boundary
- **Context map** — relationships between contexts

**Exercise (5 min):** In pairs, name 3 terms for “Order” in e-commerce vs banking.

---

## 4. Service Ownership (15 min)

- You build it, you run it
- On-call rotation per service
- API as contract to other teams

---

## 5. Common Pitfalls (10 min)

1. Distributed monolith (chatty sync calls everywhere)
2. Shared database
3. No observability before split
4. Premature microservices
5. Ignoring eventual consistency

---

## 6. Wrap-up (5 min)

**Lab preview:** Decomposition document + context map.

**Reading:** `labs/module-01/README.md`

---

## Discussion Questions

1. Why is a shared database an anti-pattern?
2. How would you split ShopMonolith differently for a 5-person startup vs 500 engineers?
