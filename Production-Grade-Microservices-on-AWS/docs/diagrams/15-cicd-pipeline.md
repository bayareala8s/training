# Diagram 15 — CI/CD Pipeline

**Module 9** — GitHub Actions to ECS.

```mermaid
flowchart LR
    subgraph Dev["Developer"]
        CODE[Push code]
    end

    subgraph GH["GitHub"]
        PR[Pull Request]
        MAIN[main branch]
    end

    subgraph CI["CI — on PR"]
        LINT[Lint / format]
        TEST[pytest unit tests]
        BUILD[docker build]
    end

    subgraph CD["CD — on merge"]
        ECR[Push to ECR<br/>linux/amd64]
        ECS[ECS force new deployment]
    end

    subgraph AWS["AWS"]
        FARGATE[Fargate tasks]
    end

    CODE --> PR
    PR --> LINT --> TEST --> BUILD
    BUILD -->|pass| MAIN
    MAIN --> ECR --> ECS --> FARGATE

    style CI fill:#cfe2ff
    style CD fill:#d4edda
```

## Deployment strategies

```mermaid
flowchart TB
    subgraph Rolling["Rolling — course default"]
        R1[Task v1] --> R2[Task v1 + v2]
        R2 --> R3[Task v2 only]
    end

    subgraph BlueGreen["Blue/Green"]
        B1[Blue env 100%] --> B2[Green env 100%]
    end

    subgraph Canary["Canary"]
        C1[90% v1 · 10% v2] --> C2[100% v2]
    end
```

| Strategy | Downtime | Rollback |
|----------|----------|----------|
| Rolling | Minimal | Previous task definition |
| Blue/Green | Near zero | Switch traffic |
| Canary | Near zero | Reduce canary % |

## Rollback runbook

```mermaid
flowchart TD
    BAD[Bad deploy detected] --> ALARM[Alarm or failed health check]
    ALARM --> REVERT[Revert Git commit OR]
    ALARM --> PREV[Deploy previous ECR image tag]
    PREV --> FORCE[ecs update-service --force-new-deployment]
    FORCE --> OK[Verify /products & demo script]
```

**Workflow files:** `.github/workflows/ci-service.yml`, `deploy-ecs.yml`
