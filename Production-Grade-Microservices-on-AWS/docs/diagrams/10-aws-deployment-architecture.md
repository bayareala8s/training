# Diagram 10 — AWS Deployment Architecture

**Module 4** — VPC, ECS Fargate, ALB (matches `infrastructure/terraform/`).

> **AWS Architecture Icons (detailed):** [aws-stencils/png/10-vpc-ecs-deployment-detail.png](aws-stencils/png/10-vpc-ecs-deployment-detail.png) · [draw.io source](aws-stencils/drawio/10-vpc-ecs-deployment-detail.drawio) · [ALB routing stencil](aws-stencils/png/10-alb-path-routing-detail.png)

## Regional deployment

```mermaid
flowchart TB
    subgraph Internet["Internet"]
        USER[Users]
    end

    subgraph AWS["AWS Region — us-east-1"]
        subgraph VPC["VPC 10.0.0.0/16"]
            subgraph Public["Public Subnets"]
                ALB[Application Load Balancer<br/>ms-course-dev-alb]
                NAT[NAT Gateway<br/>when platform_active=true]
            end

            subgraph Private["Private Subnets"]
                subgraph ECS["ECS Fargate Cluster<br/>ms-course-dev-cluster"]
                    T1[user-service task]
                    T2[product-service task]
                    T3[order-service task]
                    T4[notification-service task]
                end
            end

            SD[Cloud Map DNS<br/>ms-course-dev.local]
        end

        ECR[Amazon ECR<br/>4 repositories]
        EB[EventBridge Bus]
        DDB[(DynamoDB<br/>orders table)]
        CW[CloudWatch Logs]
        SM[Secrets Manager<br/>JWT secret]
    end

    USER -->|HTTP :80| ALB
    ALB --> T1
    ALB --> T2
    ALB --> T3
    ALB --> T4

    T1 & T2 & T3 & T4 --> NAT
    NAT --> Internet
    T3 --> ECR
    T3 --> EB
    T3 -.-> DDB
    ECS --> CW
    ECS --> SM
    T1 & T2 & T3 & T4 --- SD

    style Public fill:#cfe2ff
    style Private fill:#d4edda
    style ECS fill:#d1e7dd
```

## ALB path routing

```mermaid
flowchart LR
    ALB[ALB Listener :80]

    ALB -->|/users* /auth*| USR[user-service:8001]
    ALB -->|/products*| PRD[product-service:8002]
    ALB -->|/orders*| ORD[order-service:8003]
    ALB -->|/events*| NTF[notification-service:8004]
    ALB -->|default| DEF[Course welcome message]
```

## ECS task IAM roles

```mermaid
flowchart TB
    subgraph Roles["IAM"]
        EX[Execution Role<br/>Pull ECR · write logs]
        TASK[Task Role<br/>events:PutEvents<br/>dynamodb:* on orders table]
    end

    ECS[ECS Task] --> EX
    ECS --> TASK
```

## Terraform lifecycle

```mermaid
stateDiagram-v2
    [*] --> Stopped: aws-stop.sh
    Stopped --> Running: aws-start.sh
    Running --> Stopped: aws-stop.sh
    Stopped --> Destroyed: aws-destroy.sh
    Destroyed --> [*]

    note right of Running
        NAT + ALB + ECS tasks
        ~$1.50-3/day
    end note
    note right of Stopped
        ECS=0, no NAT/ALB
        ~$0-2/month
    end note
```
