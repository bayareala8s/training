# Lab 5 — Event-Driven Workflow

**Duration:** 4 hours | **Module 5**

## Objectives

- Place orders that emit `OrderPlaced` events
- Build notification consumer
- Switch from HTTP fan-out to EventBridge (AWS)

## Part A — Local Event Flow (60 min)

```bash
docker compose up --build
./scripts/demo-platform.sh
curl http://localhost:8004/events | jq .
```

Confirm `OrderPlaced` appears in notification event log.

## Part B — Order Service Integration (90 min)

Study `starters/python/order-service/app/events.py`:

- `EVENT_PUBLISH_MODE=http` for local
- `EVENT_PUBLISH_MODE=eventbridge` for AWS

Trace the flow in `app/main.py` after order commit.

## Part C — EventBridge (AWS) (90 min)

1. Use Terraform output `event_bus_name`
2. Create rule: `OrderPlaced` → SQS or Lambda (instructor template)
3. Set order-service env:

```
EVENT_PUBLISH_MODE=eventbridge
EVENT_BUS_NAME=<from terraform output>
```

4. Redeploy order-service to ECS

## Part D — Event Schema (30 min)

Document in `contracts/events/order-placed.json`:

```json
{
  "source": "course.orders",
  "detail-type": "OrderPlaced",
  "detail": {
    "order_id": "string",
    "user_id": "string",
    "total": 0.0,
    "items": []
  }
}
```

## Verify your work

```bash
export PLATFORM_URL=$(terraform -chdir=infrastructure/terraform output -raw platform_url)
./labs/module-05/verify.sh
```

## Deliverables

- [ ] Working local event pipeline
- [ ] Event schema committed
- [ ] Screenshot of EventBridge rule + successful test event

## Discussion Questions

1. Why not use synchronous HTTP for order confirmation email?
2. What happens if notification service is down?
