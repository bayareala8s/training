# Diagram 1 — Platform Overview

High-level view of what students build by the end of the course.

```mermaid
flowchart TB
    subgraph Clients["Clients"]
        WEB[Web / Mobile App]
        ADMIN[Admin Tools]
    end

    subgraph Edge["AWS Edge"]
        ALB[Application Load Balancer<br/>Path-based routing]
    end

    subgraph Services["Microservices — ECS Fargate"]
        USR[User Service<br/>:8001 · Auth & profiles]
        PRD[Product Service<br/>:8002 · Catalog]
        ORD[Order Service<br/>:8003 · Checkout]
        NTF[Notification Service<br/>:8004 · Events consumer]
    end

    subgraph Events["Event Layer"]
        EB[Amazon EventBridge<br/>Custom event bus]
    end

    subgraph Data["Data — per service"]
        DB1[(User DB)]
        DB2[(Product DB)]
        DB3[(Order DB)]
        DDB[(DynamoDB Orders<br/>optional AWS)]
    end

    subgraph Ops["Operations"]
        CW[CloudWatch<br/>Logs · Metrics · Alarms]
        ECR[Amazon ECR<br/>Container images]
        GHA[GitHub Actions<br/>CI/CD]
    end

    WEB --> ALB
    ADMIN --> ALB
    ALB --> USR
    ALB --> PRD
    ALB --> ORD
    ALB --> NTF

    ORD -->|HTTP GET product| PRD
    ORD -->|HTTP POST event| NTF
    ORD -->|PutEvents| EB
    EB -.->|Rule: OrderPlaced| CW

    USR --> DB1
    PRD --> DB2
    ORD --> DB3
    ORD -.-> DDB

    GHA --> ECR
    ECR --> Services
    Services --> CW

    style Clients fill:#e8f4fc
    style Services fill:#d4edda
    style Events fill:#fff3cd
    style Data fill:#f8d7da
    style Ops fill:#e2e3e5
```

## Legend

| Symbol | Meaning |
|--------|---------|
| Solid arrow | Synchronous HTTP |
| Dashed arrow | Async / optional |
| Per-service DB | Database-per-service pattern |

## Student takeaway

Each box is **owned by one team**, deployed **independently**, and observable in **production**.
