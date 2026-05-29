# Lab 8 — Observability & Reliability

**Duration:** 4 hours | **Module 8**

## Objectives

- Structured logging to CloudWatch
- Metrics and alarms
- Distributed tracing concepts (X-Ray optional)

## Part A — CloudWatch Logs (60 min)

Confirm ECS tasks ship logs to `/ecs/ms-course-dev`.

Search for `OrderPlaced` in order-service logs after placing an order.

## Part B — Dashboard (90 min)

Create CloudWatch dashboard with:

- ECS CPU / memory per service
- ALB 4xx / 5xx count
- Custom metric: orders placed (log metric filter or app metric)

## Part C — Alarms (60 min)

Create alarms:

1. ALB 5xx > 5 in 5 minutes
2. ECS CPU > 80% for 10 minutes

Define SNS topic for instructor email (optional).

## Part D — SLOs (60 min)

Define for order-service:

- **SLI:** availability of `POST /orders`
- **SLO:** 99.5% monthly
- **Error budget:** calculate example for 30 days

Write in `docs/your-name/slo-order-service.md`.

## Part E — X-Ray (Extension)

Enable `ENABLE_XRAY=true` and AWS X-Ray daemon sidecar (see AWS docs).

## Verify your work

```bash
./labs/module-08/verify.sh
```

## Deliverables

- [ ] Dashboard screenshot
- [ ] Two alarms configured
- [ ] SLO document
