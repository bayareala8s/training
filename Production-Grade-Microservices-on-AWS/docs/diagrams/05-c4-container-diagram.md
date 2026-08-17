# Diagram 5 — C4 Model: Container Diagram (Level 2)

**Module 2+** — Containers = deployable units (services, databases, message bus).

```mermaid
flowchart TB
    subgraph Platform["Microservices Platform"]
        subgraph APILayer["API Layer"]
            ALB[Application Load Balancer]
        end

        subgraph AppContainers["Application Containers — Docker"]
            USR[User Service<br/>FastAPI · REST<br/>OpenAPI: user-service.yaml]
            PRD[Product Service<br/>FastAPI · REST<br/>OpenAPI: product-service.yaml]
            ORD[Order Service<br/>FastAPI · REST<br/>OpenAPI: order-service.yaml]
            NTF[Notification Service<br/>FastAPI · event consumer]
        end

        subgraph Messaging["Messaging"]
            EB[EventBridge Bus<br/>ms-course-dev-bus]
        end

        subgraph DataStores["Data Stores"]
            DBU[(SQLite / RDS<br/>Users)]
            DBP[(SQLite / RDS<br/>Products)]
            DBO[(SQLite / DynamoDB<br/>Orders)]
        end
    end

    Person([Customer]) -->|HTTPS| ALB
    ALB --> USR
    ALB --> PRD
    ALB --> ORD
    ALB --> NTF

    ORD -->|GET /products/:id| PRD
    ORD -->|POST /events| NTF
    ORD -->|PutEvents OrderPlaced| EB

    USR --> DBU
    PRD --> DBP
    ORD --> DBO

    style AppContainers fill:#d4edda
    style Messaging fill:#fff3cd
    style DataStores fill:#f8d7da
```

## Technology mapping

| Container | Technology in course repo |
|-----------|---------------------------|
| User Service | `starters/python/user-service` |
| Product Service | `starters/python/product-service` |
| Order Service | `starters/python/order-service` |
| Notification Service | `starters/python/notification-service` |
| Event bus | `contracts/events/order-placed.json` |

## Ports (local)

| Service | Port |
|---------|------|
| User | 8001 |
| Product | 8002 |
| Order | 8003 |
| Notification | 8004 |
