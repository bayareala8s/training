# Module 5 Lecture — Event-Driven Architecture

## Sync vs Async

| Sync (HTTP) | Async (Events) |
|-------------|----------------|
| Immediate response | Decoupled in time |
| Tight coupling | Looser coupling |
| Simple debugging | Needs idempotency |

## EventBridge

- Event bus, rules, targets
- Schema registry (optional advanced topic)

## Course Event: OrderPlaced

```
Order Service → EventBridge → Notification Service
```

Local dev: HTTP to `notification-service:8004/events`

## Reliability

- At-least-once delivery
- Idempotent consumers
- Dead-letter queues (extension)

## Lab

`labs/module-05/README.md`
