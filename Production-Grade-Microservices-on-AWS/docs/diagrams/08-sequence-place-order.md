# Diagram 8 — Sequence: Place Order (Synchronous Path)

**Modules 2 & 5** — Step-by-step request flow students debug in labs.

```mermaid
sequenceDiagram
    autonumber
    actor Customer
    participant ALB as ALB / localhost
    participant User as User Service
    participant Product as Product Service
    participant Order as Order Service
    participant Notify as Notification Service

    Customer->>ALB: POST /users (register)
    ALB->>User: forward
    User-->>Customer: 201 user_id

    Customer->>ALB: POST /auth/login
    ALB->>User: forward
    User-->>Customer: 200 access_token

    Customer->>ALB: GET /products
    ALB->>Product: forward
    Product-->>Customer: 200 products list

    Customer->>ALB: POST /orders (user_id, items)
    ALB->>Order: forward

    loop For each line item
        Order->>Product: GET /products/:product_id
        Product-->>Order: 200 price, stock, name
    end

    Order->>Order: Validate stock · compute total · save order

    Order->>Notify: POST /events OrderPlaced
    Notify->>Notify: Log email · store event
    Notify-->>Order: 200 processed

    Order-->>Customer: 201 order_id, total, items

    Customer->>ALB: GET /events
    ALB->>Notify: forward
    Notify-->>Customer: 200 events list
```

## Failure scenarios (discussion)

```mermaid
sequenceDiagram
    participant Order as Order Service
    participant Product as Product Service

    Order->>Product: GET /products/:id
    Product-->>Order: 404 Not Found
    Note over Order: Return 404 to client

    Order->>Product: GET /products/:id
    Product--xOrder: Timeout
    Note over Order: 503 or retry policy
```

## Student debug checklist

1. All four health endpoints (local) or `/products` (AWS ALB)
2. Product exists before ordering
3. Check `GET /events` on notification service
