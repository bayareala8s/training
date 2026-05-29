# Diagram 4 — C4 Model: System Context (Level 1)

Shows the platform boundary and external actors. Required for **capstone** architecture submissions.

```mermaid
flowchart TB
    subgraph External["People & Systems"]
        CUST[Customer<br/>Places orders, browses catalog]
        ADMIN[Store Admin<br/>Manages products]
        OPS[Operations Engineer<br/>Monitors platform]
    end

    subgraph Platform["Course E-Commerce Platform"]
        SYS[Microservices Platform<br/>User · Product · Order · Notification]
    end

    subgraph ExternalSys["External Services"]
        EMAIL[Email Provider<br/>e.g. Amazon SES]
        IDP[Identity Provider<br/>optional OAuth]
    end

    CUST -->|HTTPS| SYS
    ADMIN -->|HTTPS| SYS
    OPS -->|AWS Console · CI/CD| SYS
    SYS -->|Send email| EMAIL
    SYS -.->|Future OAuth| IDP

    style Platform fill:#d4edda,stroke:#198754,stroke-width:2px
```

## Description (for architecture document)

The **Course E-Commerce Platform** lets customers register, browse products, and place orders. Store admins manage the catalog. The platform publishes domain events when orders are placed and sends notifications asynchronously. Operations teams deploy and monitor services on AWS ECS.

## Capstone checklist

- [ ] Name all actors
- [ ] Show single system boundary
- [ ] Label protocols (HTTPS, events)
