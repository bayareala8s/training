**Reference ADR for instructors** (and for students *after* they submit). Copying this into `submissions/lab-08/adr.md` as your work fails Lab 8 on integrity, not on Terraform.

# Architecture Decision Record

## ADR Title

Strangle the Northbridge ESB: sync balances leave first; ISO settlement stays on a certified adapter.

## Status

Accepted (reference implementation for Lab 8 — students must write their own ADR in `submissions/lab-08/adr.md`)

## Business Problem

Digital channels cannot wait six weeks for a canonical Customer map. Mobile balance lookup misses a 300 ms NFR because it hops the bus. A bad marketing transform pages settlement operators. The ISO 20022 scheme connection is certified and must not be rewritten this budget year.

## Requirements

- Balance read: ≤ 300 ms, customer-scoped, strongly consistent with core for the retail channel.
- Settlement: exactly-once posting semantics, dual-run before cutover, certified ISO map.
- New SaaS (collections) must not wait for the Customer committee.
- Marketing email is not a money movement and must not share the settlement failure domain.
- Nightly 8 GB settlement file cannot ride SOAP through the bus.
- Warehouse offline Sundays; checkout is not.

## Options Considered

### Option A

Keep the ESB as the enterprise hub. Add more maps. Lowest political friction. Fails latency, lead time, and failure isolation NFRs.

### Option B

Replace the ESB in one quarter with a single event bus for every flow. High rewrite risk on the certified ISO path. Dual-run skipped. Cost of always-on adapters ignored.

### Option C

Strangler: new **API** for balances and collections; **events** for address change and marketing; **file landing** for the 8 GB extract; **queue** for warehouse commands; **keep adapter** for ISO MQ until dual-run proves parity.

## Decision

Option C. Style is chosen per flow from NFRs, not from a platform standard. The ESB is inventory to shrink, not a destination.

## Rationale

300 ms reads are request/reply. Warehouse downtime is a buffer (message). Twenty downstreams for address change are fan-out (event). GB extracts are files. ISO is residue (adapter) with dual-run because money movement cannot skip reconciliation.

## Tradeoffs

Faster digital delivery; two runtimes during dual-run; operators must know which channel a customer is on; mapping talent still needed for ISO.

## Security Impact

New APIs use per-customer identity, not the bus service account. Dual-run logs are audit events. No agent writes to core.

## Reliability Impact

Settlement dual-run with checksums before cutover. Warehouse commands sit on a queue across Sunday. Marketing failures no longer page settlement.

## Cost Impact

No always-on Transfer Family for this slice. Dual-run compute is temporary. Do not stand up a second ESB “modernization hub.”

## Operational Impact

Runbook: which flows are strangler vs adapter. Dashboard for dual-run drift. Replay of warehouse commands is idempotent.

## Alternatives Rejected

A fails NFRs. B gambles the certified ISO path and treats marketing as an event storm without isolation.
