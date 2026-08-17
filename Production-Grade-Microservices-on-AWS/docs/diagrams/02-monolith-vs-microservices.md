# Diagram 2 — Monolith vs Microservices

Use in **Module 1** when discussing trade-offs.

## Monolith (ShopMonolith)

```mermaid
flowchart TB
    subgraph Monolith["Single Deployable — ShopMonolith"]
        UI[Web UI]
        MOD1[Users Module]
        MOD2[Catalog Module]
        MOD3[Orders Module]
        MOD4[Email Module]
        DB[(Single Database<br/>users · products · orders)]
    end

    UI --> MOD1
    UI --> MOD2
    UI --> MOD3
    MOD1 --> DB
    MOD2 --> DB
    MOD3 --> DB
    MOD4 --> DB

    style Monolith fill:#f8d7da
```

**Problems:** One deployment affects everything · Shared DB coupling · Hard to scale one feature · Blast radius on failure

---

## Microservices (Course platform)

```mermaid
flowchart TB
    subgraph MS["Independent Services"]
        S1[User Service]
        S2[Product Service]
        S3[Order Service]
        S4[Notification Service]
    end

    D1[(Users DB)]
    D2[(Products DB)]
    D3[(Orders DB)]
    EB[EventBridge]

    S1 --> D1
    S2 --> D2
    S3 --> D3
    S3 -->|events| EB
    EB --> S4

    style MS fill:#d4edda
```

**Benefits:** Independent deploy · Clear ownership · Scale order path separately · Smaller failure domains

---

## Comparison table (for slides)

| Dimension | Monolith | Microservices |
|-----------|----------|---------------|
| Deployment | One unit | Many units |
| Data | Often shared | Database per service |
| Team structure | One codebase | Service teams |
| Complexity | Lower initially | Higher always |
| Best when | Small team, unclear domain | Clear boundaries, scale needs |
