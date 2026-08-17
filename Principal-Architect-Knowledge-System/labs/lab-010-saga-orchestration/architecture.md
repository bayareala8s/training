# Lab 010: Architecture

## Overview

**Orchestration-based saga** with explicit state machine and compensations — common in enterprise order, booking, and provisioning flows.

```mermaid
stateDiagram-v2
    [*] --> Started
    Started --> PaymentReserved: reserve_payment
    PaymentReserved --> InventoryReserved: reserve_inventory
    InventoryReserved --> Shipped: create_shipment
    Shipped --> Completed
    InventoryReserved --> Compensating: inventory_fail
    PaymentReserved --> Compensating: payment_timeout
    Compensating --> Compensated: compensate_done
    Compensated --> [*]
    Completed --> [*]
```

## Happy Path Sequence

```mermaid
sequenceDiagram
    participant O as Orchestrator
    participant P as Payment
    participant I as Inventory
    participant S as Shipping

    O->>P: reserve(saga_id)
    P-->>O: OK
    O->>I: reserve(saga_id)
    I-->>O: OK
    O->>S: ship(saga_id)
    S-->>O: OK
    O->>O: mark completed
```

## Compensation Sequence

```mermaid
sequenceDiagram
    participant O as Orchestrator
    participant P as Payment
    participant I as Inventory

    O->>P: reserve OK
    O->>I: reserve FAIL
    O->>P: compensate(saga_id)
    P-->>O: released
    O->>O: mark compensated
```

## Safety and Liveness

| Property | Mechanism |
|----------|-----------|
| Safety | Compensations restore business invariants (no ghost holds) |
| Liveness | Retries + timeouts; orchestrator recovery from log |
| Idempotency | saga_id + step_id on all participant calls |

## Component Responsibilities

| Component | Responsibility |
|-----------|----------------|
| `Orchestrator` | State machine driver |
| `SagaLog` | Append-only transition log |
| `PaymentSvc` | Reserve / compensate payment |
| `InventorySvc` | Reserve / release stock |
| `ShippingSvc` | Create / cancel shipment |

## Docker Topology

Services: `orchestrator`, `payment`, `inventory`, `shipping`, `postgres`.

## Related Documentation

- [Sagas](/docs/transactions/sagas)
- [Payment Platform](/docs/system-design/payment-platform)
