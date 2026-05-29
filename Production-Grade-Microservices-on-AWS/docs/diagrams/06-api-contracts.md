# Diagram 6 — API Contracts & OpenAPI-First Development

**Module 2** — Contract-driven development between teams.

```mermaid
flowchart LR
    subgraph Design["Design Phase"]
        OA[OpenAPI YAML<br/>contracts/openapi/]
    end

    subgraph Teams["Implementation Tracks"]
        PY[Python / FastAPI]
        JV[Java / Spring Boot]
        ND[Node / NestJS]
    end

    subgraph Verify["Verification"]
        TEST[Contract tests]
        MOCK[Mock servers]
    end

    OA --> PY
    OA --> JV
    OA --> ND
    PY --> TEST
    JV --> TEST
    ND --> TEST
    OA --> MOCK

    style Design fill:#cfe2ff
```

## API surface (course platform)

```mermaid
flowchart TB
    subgraph UserAPI["User Service — :8001"]
        U1[POST /users]
        U2[POST /auth/login]
        U3["GET /users/:id"]
    end

    subgraph ProductAPI["Product Service — :8002"]
        P1[GET /products]
        P2["GET /products/:id"]
        P3[POST /products]
    end

    subgraph OrderAPI["Order Service — :8003"]
        O1[POST /orders]
        O2["GET /orders/:id"]
    end

    subgraph NotifyAPI["Notification — :8004"]
        N1[POST /events]
        N2[GET /events]
    end

    style UserAPI fill:#cfe2ff
    style ProductAPI fill:#d1e7dd
    style OrderAPI fill:#fff3cd
    style NotifyAPI fill:#f8d7da
```

## Versioning strategy (teaching slide)

```mermaid
flowchart LR
    V1["/v1/users"] --> V2["/v2/users"]
    V2 --> DEP["Deprecate v1<br/>sunset date"]

    note1[Breaking change:<br/>new required field]
    V1 -.-> note1
```

| Status code | When |
|-------------|------|
| 201 | Created |
| 400 | Validation error |
| 401 | Invalid JWT |
| 404 | Not found |
| 409 | Duplicate email / SKU |
