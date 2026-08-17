# Diagram 3 — Bounded Contexts & Context Map

**Module 1** — Domain-Driven Design foundation for the e-commerce capstone.

## Bounded contexts

```mermaid
flowchart LR
    subgraph Identity["Identity Context"]
        U1[User]
        U2[Credentials]
        U3[Session / JWT]
    end

    subgraph Catalog["Catalog Context"]
        C1[Product]
        C2[SKU]
        C3[Price]
        C4[Stock view]
    end

    subgraph Orders["Orders Context"]
        O1[Order]
        O2[OrderLine]
        O3[Checkout]
    end

    subgraph Notifications["Notifications Context"]
        N1[Email]
        N2[SMS]
        N3[Event log]
    end

    Orders -->|"Customer-Supplier<br/>GET /products/:id"| Catalog
    Orders -->|Published language<br/>OrderPlaced event| Notifications

    style Identity fill:#cfe2ff
    style Catalog fill:#d1e7dd
    style Orders fill:#fff3cd
    style Notifications fill:#f8d7da
```

## Context map (relationships)

```mermaid
flowchart TB
    ID[Identity Context<br/>User Service]
    CAT[Catalog Context<br/>Product Service]
    ORD[Orders Context<br/>Order Service]
    NOT[Notifications Context<br/>Notification Service]

    ORD -->|HTTP sync<br/>Supplier → Customer| CAT
    ORD -->|Async event<br/>OrderPlaced| NOT

    ID -.->|No direct calls in v1| ORD
    ID -.->|Future: validate user| ORD

    classDef core fill:#d4edda,stroke:#333
    class ID,CAT,ORD,NOT core
```

## Ubiquitous language (examples)

| Context | Terms students must use consistently |
|---------|--------------------------------------|
| Identity | User, register, login, JWT |
| Catalog | Product, SKU, list price, stock |
| Orders | Order, line item, placed, total |
| Notifications | OrderPlaced, confirmation, subscriber |

## Anti-pattern to call out

```mermaid
flowchart LR
    ORD[Order Service] -->|SQL JOIN| SHARED[(Shared DB)]
    PRD[Product Service] --> SHARED

    style SHARED fill:#f8d7da
```

**Never** let Order Service query Product tables directly — use **API** or **events**.
