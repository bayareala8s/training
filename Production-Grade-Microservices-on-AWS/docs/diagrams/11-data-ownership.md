# Diagram 11 — Data Ownership (Database per Service)

**Module 6** — No shared database anti-pattern.

```mermaid
flowchart TB
    subgraph Services["Services — each owns its data"]
        USR[User Service]
        PRD[Product Service]
        ORD[Order Service]
        NTF[Notification Service]
    end

    subgraph Databases["Private data stores"]
        DBU[(users.db / RDS<br/>ONLY User Service)]
        DBP[(products.db / RDS<br/>ONLY Product Service)]
        DBO[(orders.db / DynamoDB<br/>ONLY Order Service)]
        MEM[(In-memory event log<br/>ONLY Notification)]
    end

    USR -->|read/write| DBU
    PRD -->|read/write| DBP
    ORD -->|read/write| DBO
    NTF -->|read/write| MEM

    ORD -.->|❌ NO direct SQL| DBP
    PRD -.->|❌ NO direct SQL| DBO

    style Databases fill:#d4edda
```

## How Order gets product data

```mermaid
flowchart LR
    ORD[Order Service]
    PRD[Product Service]
    API["GET /products/:id"]
    DBP[(Product DB)]

    ORD -->|HTTP only| API
    API --> PRD
    PRD --> DBP

    style API fill:#cfe2ff
```

## DynamoDB orders table (AWS extension)

| Attribute | Type | Notes |
|-----------|------|-------|
| order_id | String (PK) | Partition key |
| user_id | String | GSI candidate |
| total | Number | |
| items | List/Map | Embedded or separate table |

**Table name:** `ms-course-dev-orders`
