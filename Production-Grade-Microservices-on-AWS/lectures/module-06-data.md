# Module 6 — Data Management & Distributed Consistency

**Production-Grade Microservices on AWS · BayAreaLa8s**

| | |
|---|---|
| **Duration** | 90 minutes lecture + 4 hours lab |
| **Week** | 6 of 10 |
| **Prerequisites** | Modules 1–5 |

---

## Learning Objectives

Students will be able to:

1. Apply **database-per-service** and explain why cross-service SQL joins fail at scale.
2. Choose between **DynamoDB** and **RDS** for course and capstone workloads.
3. Distinguish **strong** vs **eventual** consistency across service boundaries.
4. Compare **saga** patterns: choreography vs orchestration.
5. Design **stock decrement** and order placement without a shared transaction.

---

## Session Agenda

| Segment | Time | Topic |
|---------|------|--------|
| Data ownership | 20 min | Per-service stores, API access |
| DynamoDB vs RDS | 20 min | Access patterns, operations |
| Consistency models | 25 min | ACID local, eventual global |
| Saga patterns | 20 min | Happy path, compensation |
| Exercise & wrap-up | 5 min | Stock decrement design |

**Diagrams:** [11-data-ownership](../docs/diagrams/11-data-ownership.md) · [12-saga-consistency](../docs/diagrams/12-saga-consistency.md)

---

## 1. Database-per-Service (20 minutes)

### 1.1 Principle

Each microservice **owns** its data:

- Only that service’s code may **write** its database.
- Other services access data via **API** or **events**.

```
✅ Order → GET /products/:id → Product Service → products.db
❌ Order → JOIN products ON ...
```

See [11-data-ownership](../docs/diagrams/11-data-ownership.md).

### 1.2 Course data stores

| Service | Local (dev) | AWS (course) |
|---------|-------------|--------------|
| User | SQLite `users.db` | SQLite in task (lab) / RDS extension |
| Product | SQLite `products.db` | SQLite in task |
| Order | SQLite `orders.db` | SQLite + optional **DynamoDB** `ms-course-dev-orders` |
| Notification | In-memory event log | In-memory |

**DynamoDB table:** Partition key `order_id`—see Terraform `aws_dynamodb_table.orders`.

### 1.3 Denormalization & read models

Consumers may store **copies** of data they need (e.g. `product_name` on order line items) to avoid chatty sync calls—accept **staleness** with clear rules.

### 1.4 Reporting and analytics

Operational OLTP schemas ≠ warehouse schemas. Use **CDC**, **events**, or **ETL** to analytics—never slow down order path with reporting joins.

---

## 2. DynamoDB vs RDS (20 minutes)

### 2.1 Decision matrix

| Factor | DynamoDB | RDS (PostgreSQL/MySQL) |
|--------|----------|------------------------|
| **Scale model** | Horizontal, single-digit ms | Vertical + read replicas |
| **Query flexibility** | Key/access pattern driven | SQL, joins, ad hoc |
| **Operations** | Serverless capacity modes | Patch, backup, Multi-AZ |
| **Transactions** | Single-table / multi-item in account | Full ACID SQL |
| **Course orders** | Optional AWS extension | Catalog/reporting extension |

### 2.2 DynamoDB modeling basics

| Concept | Orders example |
|---------|----------------|
| **Partition key** | `order_id` |
| **Sort key** | (optional) `created_at` |
| **GSI** | Query by `user_id` |
| **Item design** | Embed `items[]` or separate table |

**Access pattern first:** List queries you need before choosing keys.

### 2.3 When teams pick RDS

- Complex reporting inside service boundary
- Mature ORM/migration tooling (Flyway, Alembic)
- Existing DBA practice

**Hybrid architectures** are normal: DynamoDB for hot path, RDS for admin/reporting service.

---

## 3. Consistency Models (25 minutes)

### 3.1 Within one service

Use **ACID transactions** inside User, Product, or Order database:

```python
# Pseudocode — single DB session
with session.begin():
    order = Order(...)
    session.add(order)
```

### 3.2 Across services

No distributed two-phase commit in this course stack. Accept **eventual consistency**:

1. Order created and persisted.
2. `OrderPlaced` event published.
3. Notification sends email (seconds later).
4. Analytics service updates dashboard (minutes later).

**User experience:** Show “Order confirmed” after step 1; email is best-effort async.

### 3.3 CAP theorem (practical framing)

During network partition, choose **availability** vs **consistency** for each operation. E-commerce checkout often favors **availability** with business compensations.

### 3.4 Read-your-writes

User may not see their order in a **replica** immediately. Mitigations:

- Read from primary after write
- Client holds `order_id` from 201 response
- UI optimistic state

---

## 4. Saga Patterns (20 minutes)

### 4.1 Problem

Business process spans **Order** (debit stock) + **Payment** (charge card). Cannot use one DB transaction.

### 4.2 Choreography saga (events)

Each service listens and reacts:

```
OrderCreated → Payment processes → PaymentSucceeded → Order marks paid
PaymentFailed → Order cancels / compensates
```

**Pros:** Loose coupling. **Cons:** Hard to see global state; debugging scattered.

### 4.3 Orchestration saga

**Step Functions** or saga coordinator tells each step what to do.

**Pros:** Visible workflow, timeouts centralized. **Cons:** Coordinator becomes critical component.

### 4.4 Compensation

| Forward action | Compensating action |
|----------------|---------------------|
| Reserve inventory | Release reservation |
| Charge payment | Refund |
| Create shipment | Cancel shipment |

Not all steps are compensatable (email sent)—design **idempotent** and **reversible** where possible.

### 4.5 Course scope: inventory exercise

**Scenario:** Product has `stock: 10`. Two concurrent orders for 7 units each.

| Approach | Outcome |
|----------|---------|
| No locking | Oversell |
| Optimistic locking in Product | Second order fails 409 |
| Reserve via event | Eventual stock alignment |

**Class exercise (10 min):** Whiteboard choreography for decrement stock + create order + rollback on payment failure.

---

## Lab & Assignment

- **Lab 06:** [`labs/module-06/README.md`](../labs/module-06/README.md)
- **Assignment 06:** [`assignments/module-06.md`](../assignments/module-06.md)

### Summary

- **Own your data**; integrate with APIs and events.
- **Pick storage** by access pattern, not hype.
- **Sagas** manage multi-step business processes without a shared database.

---

## Discussion Questions

1. Why can’t Order Service use a foreign key to Product’s table?
2. When is eventual consistency unacceptable for a user-facing read?
3. Choreography vs orchestration—which fits a 4-service capstone?
4. How would you implement idempotent stock decrement?

---

*BayAreaLa8s · Production-Grade Microservices on AWS*
