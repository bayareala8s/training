# State & Failover Strategy — Option 3

## State

| Item | Choice | Rationale |
|------|--------|-----------|
| State backend | S3 in primary region (shared bucket OK) | Encrypt + versioning |
| State keys | `.../primary/` and `.../secondary/` | **Separate state per region** |
| Locking | DynamoDB | Prevent concurrent apply during failover drill |

**Why separate state:** limits blast radius; primary apply cannot accidentally destroy secondary.

## Config strategy

- Same module source and variable shapes for primary/secondary.
- Region-specific CIDRs and AZs via variables (no hard-coded region in modules).
- Tags: `DRRole=primary|secondary`, `Capstone=option-03`.

## Failover modes

1. **Tabletop** — walk runbook; no DNS cutover.
2. **Warm standby** — secondary VPC exists; start compute; update app DNS (manual or Route53).
3. **Pilot light** — secondary VPC only; scale compute on failover (this lab default with `enable_lab_compute=false` on secondary).

## Data

This capstone focuses on **network foundation DR**. Database replication (RDS cross-region) is an optional stretch and incurs significant cost—document only unless instructor approves.
