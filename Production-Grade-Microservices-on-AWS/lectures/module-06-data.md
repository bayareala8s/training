# Module 6 Lecture — Data Management

## Database-per-Service

Each service owns its schema. **No cross-DB joins.**

## DynamoDB vs RDS

| DynamoDB | RDS |
|----------|-----|
| Scale, key-value access | Complex queries, ACID |
| Orders, sessions | Reporting, catalog (sometimes) |

## Consistency

- **Strong** within one service transaction
- **Eventual** across services via events

## Saga Pattern

Choreography (events) vs orchestration (coordinator).

**Exercise:** Design stock decrement for order flow.

## Lab

`labs/module-06/README.md`
