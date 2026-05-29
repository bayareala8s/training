# Diagram 9 — Event-Driven Architecture

**Module 5** — Async decoupling with `OrderPlaced`.

## Choreography (course default)

```mermaid
flowchart LR
    ORD[Order Service<br/>Publisher]
    EB[EventBridge<br/>Event Bus]
    NTF[Notification Service<br/>Consumer]
    LOG[CloudWatch Logs<br/>Audit target]
    ANA[Analytics Service<br/>Future]

    ORD -->|PutEvents<br/>detail-type: OrderPlaced| EB
    EB -->|Rule match| NTF
    EB -->|Rule match| LOG
    EB -.->|Future| ANA

    style ORD fill:#fff3cd
    style EB fill:#cfe2ff
    style NTF fill:#d4edda
```

## Event schema

```mermaid
classDiagram
    class OrderPlaced {
        +string order_id
        +string user_id
        +float total
        +OrderItem[] items
    }
    class OrderItem {
        +string product_id
        +string product_name
        +int quantity
    }
    OrderPlaced --> OrderItem
```

**Contract file:** `contracts/events/order-placed.json`

## Local vs AWS publishing

```mermaid
flowchart TB
    subgraph Local["Local — EVENT_PUBLISH_MODE=http"]
        O1[Order Service] -->|POST /events| N1[Notification Service]
    end

    subgraph AWS["AWS — optional EventBridge"]
        O2[Order Service] -->|PutEvents| EB[EventBridge]
        EB --> N2[Notification via ALB HTTP]
        EB --> CW[CloudWatch Logs]
    end

    style Local fill:#d4edda
    style AWS fill:#cfe2ff
```

## Sync vs async (why events?)

| Approach | Coupling | If notification is down |
|----------|----------|-------------------------|
| Sync HTTP call from Order | Tight | Order fails |
| Async event | Loose | Order succeeds; retry/DLQ |

## Idempotency note

```mermaid
flowchart LR
    E1[OrderPlaced event] --> C1[Consumer]
    E2[Duplicate event] --> C1
    C1 --> IDEM{Seen order_id?}
    IDEM -->|yes| SKIP[Skip]
    IDEM -->|no| PROC[Process]
```
