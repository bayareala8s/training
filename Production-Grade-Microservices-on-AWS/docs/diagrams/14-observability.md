# Diagram 14 — Observability (Three Pillars)

**Module 8** — CloudWatch, logs, metrics, SLOs.

```mermaid
flowchart TB
    subgraph Services["Microservices"]
        S1[user-service]
        S2[product-service]
        S3[order-service]
        S4[notification-service]
    end

    subgraph Pillars["Three Pillars"]
        LOGS[Logs<br/>What happened?]
        METRICS[Metrics<br/>How much? How fast?]
        TRACES[Traces<br/>Where did time go?]
    end

    subgraph AWS["AWS Observability"]
        CW[CloudWatch Logs<br/>/ecs/ms-course-dev]
        CWM[CloudWatch Metrics<br/>CPU · memory · ALB 5xx]
        DASH[Dashboards]
        ALARM[Alarms → SNS]
        XRAY[X-Ray optional]
    end

    S1 & S2 & S3 & S4 --> LOGS
    S1 & S2 & S3 & S4 --> METRICS
    S1 & S2 & S3 & S4 -.-> TRACES

    LOGS --> CW
    METRICS --> CWM
    TRACES -.-> XRAY
    CWM --> DASH
    CWM --> ALARM
```

## SLO example (order service)

```mermaid
flowchart LR
    SLI[SLI<br/>Successful POST /orders]
    SLO[SLO<br/>99.5% over 30 days]
    EB[Error Budget<br/>0.5% = ~3.6h downtime]

    SLI --> SLO --> EB
```

## Incident response flow

```mermaid
flowchart TD
    A[Alarm fires] --> B[On-call notified]
    B --> C{Triage logs & metrics}
    C --> D[Mitigate<br/>rollback · scale]
    D --> E[Postmortem<br/>blameless]
```

## Key log queries (teaching)

| Goal | Where |
|------|-------|
| Failed orders | `/ecs/ms-course-dev` filter `order-service` |
| OrderPlaced events | `/eventbridge/ms-course-dev/orders` |
| ALB errors | ALB 5xx metric |
