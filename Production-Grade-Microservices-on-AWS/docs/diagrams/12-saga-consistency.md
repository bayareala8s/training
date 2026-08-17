# Diagram 12 — Saga Pattern & Eventual Consistency

**Module 6** — Stock decrement after order (extension lab).

## Problem: cross-service transaction

```mermaid
flowchart TB
    P[Place Order] --> D[Decrement Stock]
    P -.->|Cannot use single DB transaction| D
```

## Choreography saga (recommended teaching example)

```mermaid
sequenceDiagram
    participant Order as Order Service
    participant Bus as EventBridge
    participant Product as Product Service
    participant Notify as Notification

    Order->>Order: Create order (committed)
    Order->>Bus: OrderPlaced
    Bus->>Notify: deliver
    Bus->>Product: OrderPlaced (future)
    Product->>Product: Decrement stock
    alt Stock insufficient
        Product->>Bus: StockReservationFailed
        Bus->>Order: Compensate — cancel order
    end
```

## Saga states

```mermaid
stateDiagram-v2
    [*] --> OrderPlaced
    OrderPlaced --> StockReserved: success
    OrderPlaced --> OrderCancelled: compensation
    StockReserved --> [*]
    OrderCancelled --> [*]
```

## Strong vs eventual

| Pattern | Consistency | Complexity |
|---------|-------------|------------|
| Single monolith DB | Strong | Low |
| 2PC across DBs | Strong | Very high |
| Saga + events | Eventual | Medium |
| Read-your-writes via API | Per-service | Low |

## CAP theorem (one slide)

```mermaid
mindmap
  root((Distributed System))
    Consistency
      All nodes same data
    Availability
      Every request gets response
    Partition tolerance
      Network splits happen
    Note
      Pick 2 of 3 in practice
```
