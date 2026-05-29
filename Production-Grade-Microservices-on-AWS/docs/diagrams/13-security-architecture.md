# Diagram 13 — Security Architecture

**Module 7** — JWT, IAM, secrets, network.

## Authentication flow (JWT)

```mermaid
sequenceDiagram
    actor User
    participant API as User Service
    participant DB as User DB
    participant SVC as Other Service

    User->>API: POST /users (email, password)
    API->>DB: store bcrypt hash
    API-->>User: 201

    User->>API: POST /auth/login
    API->>DB: verify hash
    API-->>User: 200 access_token JWT

    User->>SVC: POST /products + Authorization Bearer
    SVC->>SVC: Validate JWT signature & expiry
    SVC-->>User: 201 or 401
```

## JWT structure (teaching)

```mermaid
flowchart LR
    JWT[JWT Token]
    JWT --> H[Header<br/>alg: HS256]
    JWT --> P[Payload<br/>sub: user_id · exp]
    JWT --> S[Signature<br/>HMAC secret]

    SEC[Secrets Manager<br/>JWT_SECRET] -.-> S
```

## ECS IAM — two roles

```mermaid
flowchart TB
    subgraph Task["ECS Task"]
        APP[Application container]
    end

    subgraph ExecutionRole["Execution Role"]
        E1[ecr:GetAuthorizationToken]
        E2[logs:CreateLogStream]
    end

    subgraph TaskRole["Task Role — least privilege"]
        T1[events:PutEvents on course bus]
        T2[dynamodb:* on orders table only]
    end

    APP --> ExecutionRole
    APP --> TaskRole

    style TaskRole fill:#d4edda
```

## Network security

```mermaid
flowchart TB
    INTERNET[Internet]
    ALB_SG[ALB Security Group<br/>Inbound: 80 from 0.0.0.0/0]
    ECS_SG[ECS Security Group<br/>Inbound: from ALB + self]
    TASKS[ECS Tasks<br/>No public IP]

    INTERNET --> ALB_SG
    ALB_SG --> ECS_SG
    ECS_SG --> TASKS
    TASKS -->|egress via NAT| INTERNET
```

## Security checklist mapping

| Control | Implementation |
|---------|----------------|
| Secrets not in Git | Secrets Manager + `.env.example` |
| Password hashing | bcrypt in user-service |
| Least privilege IAM | Scoped task role |
| TLS in production | HTTPS on ALB (extension) |
