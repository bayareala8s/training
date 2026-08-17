# Diagram 16 — Capstone: E-Commerce Platform

**Module 10** — Full reference architecture for student submissions.

## End-state architecture

```mermaid
flowchart TB
    subgraph Actors["Actors"]
        C[Customer]
        A[Admin]
    end

    subgraph Presentation["Edge"]
        ALB[ALB + HTTPS]
    end

    subgraph Core["Core Services"]
        USR[User Service<br/>Identity]
        PRD[Product Service<br/>Catalog]
        INV[Inventory Service<br/>optional extension]
        ORD[Order Service<br/>Checkout]
        PAY[Payment Service<br/>banking track]
        NTF[Notification Service]
        ANA[Analytics Service<br/>SaaS track]
    end

    subgraph Platform["Platform Services"]
        EB[EventBridge]
        CW[CloudWatch]
        GHA[GitHub Actions]
    end

    C --> ALB
    A --> ALB
    ALB --> USR & PRD & ORD & NTF
    ORD --> PRD
    ORD --> EB
    EB --> NTF
    EB -.-> ANA
    GHA --> Core
    Core --> CW

    style Core fill:#d4edda
```

## Capstone track options

```mermaid
flowchart LR
    subgraph Ecom["Option 1 — E-Commerce ✓ default"]
        E1[User · Product · Inventory · Order · Notify]
    end

    subgraph Bank["Option 2 — Banking"]
        B1[Customer · Payment · Fraud · Notify]
    end

    subgraph SaaS["Option 3 — SaaS"]
        S1[Auth · Billing · UserMgmt · Analytics]
    end
```

## Deliverables map

```mermaid
mindmap
  root((Capstone))
    Diagrams
      C4 Context
      C4 Container
      AWS Deployment
    Code
      3 plus services
      OpenAPI specs
    Operations
      CI/CD green
      Dashboards
      Cost analysis
    Demo
      15 to 20 minutes live
```

## Grading rubric (visual)

```mermaid
pie title Capstone Points (100)
    "Architecture 20" : 20
    "Implementation 25" : 25
    "Security 15" : 15
    "Observability 15" : 15
    "CI/CD 15" : 15
    "Demo & docs 10" : 10
```

See `capstone/rubrics.md` for full criteria.
