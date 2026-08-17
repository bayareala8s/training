# Capstone Architecture Diagram Guide

Submit three diagrams. **Start from course templates** in [docs/diagrams/](../../docs/diagrams/README.md).

## 1. Context Diagram (C4 Level 1)

- **Template:** [04-c4-system-context.md](../../docs/diagrams/04-c4-system-context.md)
- Actors: Customer, Admin, External Payment (optional)
- System: Your platform boundary

## 2. Container Diagram (C4 Level 2)

- **Template:** [05-c4-container-diagram.md](../../docs/diagrams/05-c4-container-diagram.md)
- ALB, each microservice, EventBridge, databases

## 3. Deployment Diagram

- **Template:** [10-aws-deployment-architecture.md](../../docs/diagrams/10-aws-deployment-architecture.md)
- VPC subnets, ECS Fargate, ECR, DynamoDB, CloudWatch

## Optional fourth diagram

- **Sequence:** [08-sequence-place-order.md](../../docs/diagrams/08-sequence-place-order.md)
- **Events:** [09-event-driven-flow.md](../../docs/diagrams/09-event-driven-flow.md)

## Export

See [EXPORT-GUIDE.md](../../docs/diagrams/EXPORT-GUIDE.md) — Mermaid Live → PNG for slides.

## Grading emphasis

Clarity of data ownership and event flows matters more than artistic quality.
