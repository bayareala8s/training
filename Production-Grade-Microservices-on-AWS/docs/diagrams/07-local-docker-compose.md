# Diagram 7 — Local Development (Docker Compose)

**Module 3** — How services run on a student laptop.

```mermaid
flowchart TB
    subgraph Host["Developer Machine"]
        subgraph Compose["docker compose"]
            USR[user-service<br/>:8001]
            PRD[product-service<br/>:8002]
            ORD[order-service<br/>:8003]
            NTF[notification-service<br/>:8004]
        end

        VOL1[(volume: user-data)]
        VOL2[(volume: product-data)]
        VOL3[(volume: order-data)]
    end

    DEV[Developer<br/>curl · browser] --> USR
    DEV --> PRD
    DEV --> ORD
    DEV --> NTF

    USR --> VOL1
    PRD --> VOL2
    ORD --> VOL3

    ORD -->|PRODUCT_SERVICE_URL| PRD
    ORD -->|EVENT_HTTP_ENDPOINT| NTF

    style Compose fill:#d4edda
```

## Multi-stage Docker build

```mermaid
flowchart LR
    subgraph Stage1["Builder stage"]
        B1[python:3.12-slim]
        B2[pip install requirements]
    end

    subgraph Stage2["Runtime stage"]
        R1[python:3.12-slim]
        R2[Copy site-packages only]
        R3[Copy app code]
    end

    B1 --> B2 --> R1
    R2 --> R3
    R3 --> IMG[Small production image]

    style Stage2 fill:#d4edda
```

## Commands

```bash
docker compose up --build
./scripts/demo-platform.sh
```
