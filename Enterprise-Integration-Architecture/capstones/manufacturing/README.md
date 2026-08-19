# Capstone 4 — Global Supply Chain Integration Platform

**Final and hardest project.** You must explain **every** integration choice.

## Scenario

Atlas Manufacturing (fiction) integrates suppliers, factories, warehouses, ERP, logistics, inventory, analytics.

Partner capabilities differ: REST, SFTP, batch files. Legacy ERP still needs an **ESB/adapter**. Internal systems use events and queues.

## Target shape (constraint, not a completed design)

```text
Suppliers → API / SFTP / Files → Enterprise Integration Platform
        → APIs / Events / Queues → ERP / Factory / Warehouse / Logistics / Analytics
```

## AI agent — Supply Chain Operations Agent

- Which suppliers haven't delivered today's files?
- Why is shipment 92841 delayed?
- Which integrations failed today?
- Show suppliers with repeated failures.
- Retry Supplier ABC transaction — **HITL**

## Final architecture challenge

For each flow: Why API? Why SFTP? Why queue? Why event? Why adapter? Why AI agent?

If you cannot answer, the design is incomplete.

## NFRs

Multi-partner isolation, nightly GB-scale files, plant networks, ERP change windows, cost of always-on SFTP, replay without double-shipping.

## Deliverables

Full portfolio. This capstone should reference patterns by name from Module 10.

## Working slice

```bash
./scripts/lab_up.sh manufacturing
python3 scripts/validate_lab.py manufacturing
./scripts/lab_down.sh manufacturing
```

Upload `inbound/ACME/daily.csv`, then `GET /suppliers/missing` (BOLTCO and YIELD remain). `GET /shipments/92841` is DELAYED. `RequestRetry` stays PENDING until `POST /approve`.

