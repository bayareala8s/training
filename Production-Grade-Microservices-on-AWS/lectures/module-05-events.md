# Module 5 — Event-Driven Architecture & Asynchronous Integration

**Production-Grade Microservices on AWS · BayAreaLa8s**

| | |
|---|---|
| **Duration** | 90 minutes lecture + 4 hours lab |
| **Week** | 5 of 10 |
| **Prerequisites** | Module 4, order flow from Module 2 |

---

## Learning Objectives

Students will be able to:

1. Compare **synchronous HTTP** and **asynchronous events** for coupling, latency, and failure modes.
2. Describe **Amazon EventBridge** buses, rules, patterns, and targets.
3. Implement and verify the **`OrderPlaced`** contract (`contracts/events/order-placed.json`).
4. Explain **at-least-once delivery**, **idempotent consumers**, and **dead-letter queues**.
5. Contrast **local HTTP event mode** vs **AWS EventBridge** in the course platform.

---

## Session Agenda

| Segment | Time | Topic |
|---------|------|--------|
| Sync vs async | 20 min | Coupling, choreography |
| EventBridge | 25 min | Bus, rules, schemas |
| OrderPlaced deep dive | 25 min | Publisher, consumer, demo |
| Reliability patterns | 15 min | Idempotency, DLQ, ordering |
| Wrap-up | 5 min | Lab 05 |

**Diagrams:** [09-event-driven-flow](../docs/diagrams/09-event-driven-flow.md) · [AWS EventBridge stencil](../docs/diagrams/aws-stencils/png/09-eventbridge-order-flow.png)

---

## 1. Synchronous vs Asynchronous (20 minutes)

### 1.1 Comparison

| Dimension | Sync (HTTP) | Async (events) |
|-----------|-------------|----------------|
| **Coupling in time** | Caller waits | Caller continues |
| **Coupling in space** | Must know endpoint | Knows bus/topic name |
| **Failure impact** | Cascading timeouts | Consumer can catch up |
| **Debugging** | Single trace path | Needs correlation IDs |
| **Consistency** | Immediate read-your-writes | Eventual |

### 1.2 When to use which

| Use sync HTTP when | Use events when |
|--------------------|-----------------|
| Need immediate response (GET product price) | Side effects (email, analytics) |
| Simple request/response | Many subscribers |
| Strong user-facing latency SLA | Peak buffering / decoupling |
| Transaction within one service | Cross-service notifications |

**Course pattern:** Order **sync** calls Product for price/stock; **async** notifies Notification of `OrderPlaced`.

### 1.3 Choreography vs orchestration

| Style | Description | Course |
|-------|-------------|--------|
| **Choreography** | Services react to events without central coordinator | Default—Order publishes, Notification reacts |
| **Orchestration** | Central workflow engine (Step Functions) | Extension for complex sagas |

See [12-saga-consistency](../docs/diagrams/12-saga-consistency.md) (Module 6 preview).

---

## 2. Amazon EventBridge (25 minutes)

### 2.1 Event-driven bus model

```
Publisher → Event bus → Rules (pattern match) → Targets
```

**Course bus:** `ms-course-dev-bus` (custom event bus in Terraform).

### 2.2 Event envelope

EventBridge events include:

- `source` — e.g. `course.order-service`
- `detail-type` — e.g. `OrderPlaced`
- `detail` — JSON payload (your schema)
- `time`, `id`, `region`, `account`

### 2.3 Rules and targets

| Rule concept | Example |
|--------------|---------|
| **Event pattern** | `detail-type: OrderPlaced` |
| **Target** | CloudWatch Logs, Lambda, HTTP (via API Destinations), SQS |

**Lab:** Order task role has `events:PutEvents`; rules route to audit logs and (via HTTP) notification path.

### 2.4 Schema registry (extension)

EventBridge Schema Registry can generate code bindings—optional for enterprises with strict contracts.

---

## 3. OrderPlaced — End-to-End (25 minutes)

### 3.1 Contract

File: [`contracts/events/order-placed.json`](../contracts/events/order-placed.json)

```json
{
  "order_id": "ord_123",
  "user_id": "usr_abc",
  "total": 59.98,
  "items": [
    {
      "product_id": "prod_1",
      "product_name": "Widget",
      "quantity": 2
    }
  ]
}
```

**Published language:** Notification context accepts this shape; version with `schema_version` field for evolution.

### 3.2 Publisher — Order Service

Code path: `starters/python/order-service/app/events.py`

| Mode | `EVENT_PUBLISH_MODE` | Behavior |
|------|----------------------|----------|
| **Local** | `http` | `POST` to Notification `/events` |
| **AWS** | Can use EventBridge `PutEvents` | Bus name in env |

### 3.3 Consumer — Notification Service

- Receives event payload
- Logs simulated email
- Stores in-memory event log (`GET /events` for demos)

### 3.4 Demo flow

```bash
# Local
docker compose up -d
./scripts/demo-platform.sh
curl http://localhost:8004/events

# AWS
./scripts/aws-start.sh
./scripts/verify-aws-labs.sh
```

### 3.5 Class diagram

Use Mermaid class diagram in [09-event-driven-flow](../docs/diagrams/09-event-driven-flow.md) for `OrderPlaced` / `OrderItem` fields.

---

## 4. Reliability Patterns (15 minutes)

### 4.1 Delivery semantics

| Guarantee | Meaning |
|-----------|---------|
| **At-most-once** | May lose, never duplicate |
| **At-least-once** | May duplicate, rarely lose (EventBridge/SQS typical) |
| **Exactly-once** | Hard—requires dedup + transactions |

**Assume at-least-once** in production consumers.

### 4.2 Idempotent consumer

```
On event:
  if already_processed(order_id):
    return 200 OK
  else:
    send_email()
    mark_processed(order_id)
```

Use **DynamoDB conditional write** or idempotency key table in capstone.

### 4.3 Dead-letter queues (DLQ)

Failed processing after N retries → **DLQ** for manual inspection and replay.

**Extension:** SQS queue as EventBridge target with DLQ on Lambda consumer.

### 4.4 Ordering

EventBridge **does not guarantee global order** across partitions. Design for **per-aggregate** ordering if needed (e.g. FIFO SQS with `order_id` as group ID).

### 4.5 Observability

Log `event_id`, `order_id`, `correlation_id` in structured JSON (Module 8).

---

## Lab & Assignment

- **Lab 05:** [`labs/module-05/README.md`](../labs/module-05/README.md)
- **Assignment 05:** [`assignments/module-05.md`](../assignments/module-05.md)

### Summary

- Events **decouple** Notification from Order’s latency and availability.
- **Contracts** and **idempotency** are non-negotiable for async production systems.
- Course demonstrates **HTTP locally**, **EventBridge on AWS**—same business semantics.

---

## Discussion Questions

1. Should Order Service wait for Notification to send email before returning 201? Why or why not?
2. How would you detect duplicate `OrderPlaced` processing?
3. When would Step Functions orchestration beat choreography?
4. What belongs in `detail-type` vs `detail` payload?

---

*BayAreaLa8s · Production-Grade Microservices on AWS*
