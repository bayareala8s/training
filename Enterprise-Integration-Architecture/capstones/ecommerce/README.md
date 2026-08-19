# Capstone 2 — Event-Driven Commerce Platform

**Domain:** Retail / e-commerce  
Design first. The failure scenario is mandatory.

## Systems

Web, mobile, orders, payments, inventory, warehouse, shipping, notifications, analytics.

## Events you must have a story for

OrderCreated, PaymentAuthorized, InventoryReserved, OrderPacked, OrderShipped, OrderDelivered.

## Architecture concepts to apply

Saga, eventual consistency, compensation, event replay, idempotency, failure isolation.

## Failure scenario (required)

**Payment succeeds. Inventory reservation fails.**

Determine recovery: compensating transaction, user UX, support playbook, idempotent refund/release, what you do **not** replay.

## AI agent

Customer service agent: “Where is order 12345?”, “Why delayed?”, “What system is causing the delay?”

Governed tools to status APIs — not warehouse DB.

## Existing architecture

Monolithic checkout that HTTP-calls payments and inventory. Analytics JDBC to the checkout database. Email sent inside the checkout transaction.

## NFRs

- Checkout first response < 2s (acceptance, not shipment).
- Inventory and email isolation.
- No lost paid-but-unreserved orders.

## Deliverables

Same portfolio set as Capstone 1. ADRs must name **Saga** and **Compensating Transaction**.

## Working slice

```bash
./scripts/lab_up.sh ecommerce
python3 scripts/validate_lab.py ecommerce
./scripts/lab_down.sh ecommerce
```

POST `/orders` with `amount: 20` completes. POST with `failInventory: true` (or amount `13.13`) authorizes payment then compensates to `COMPENSATED`. Customer-service tools call `GetOrderStatus` — not the warehouse database.

