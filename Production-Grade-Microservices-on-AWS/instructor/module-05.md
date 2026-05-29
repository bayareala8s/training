# Instructor Notes — Module 5

## Whiteboard flow

Order Service → EventBridge → Rule → Notification (SQS/Lambda/HTTP)

## Live demo

1. `curl` place order
2. `curl localhost:8004/events`

## AWS transition

Set `EVENT_PUBLISH_MODE=eventbridge` only after bus exists.
