# INCIDENT-805 — Instructor solution

**Do not share this file with students before they submit a worksheet.**

## RCA

Jordan set `logging.level.com.baypay=DEBUG` on `pay-prod-east-2` to “trace Avery.” At DEBUG, `Payment.toString()` (and related entity logging) **walks the graph**. Each create allocates huge `String` / `char[]` trees. Allocation rate is **~1.8 GB/s**. G1 young pauses reach **hundreds of milliseconds** (excerpt max 640 ms). Old generation stays ~228 MB.

The histogram is **short-lived** `String` / `[C]`, not the INCIDENT-802 retained `IdempotencyRecord` set. This is not a GC bug and not a leak. east-1 stays INFO and healthy. Hikari and the database are fine.

## Stabilization

1. **Revert the log level** on east-2 to INFO (remove the DEBUG overlay).
2. Do not set DEBUG on east-1.
3. Do **not** bounce Postgres.
4. Do not bounce `dmgr-east`.
5. Do not switch collectors or raise `-Xmx` as the first move.
6. Optional: bounce the canary only if log buffers or pinned threads do not drain; the allocation storm should stop when DEBUG is off.

## Remediation

- Do **not** `toString()` JPA / domain entities on the hot path.
- Rate-limit DEBUG (per logger, sampled correlation ids).
- Structured fields: `paymentId`, `customerId`, status — not the graph.
- Require a change ticket and a CPU/allocation gate for production log-level overlays.
- Add a test or pre-prod check that DEBUG on `com.baypay` cannot exceed a bytes/s budget.

## Evidence students should have used

| Gate | What it shows |
|---|---|
| Dashboard | Allocation 1.8 GB/s; pause p99 420 ms; old gen flat; DEBUG overlay; log lines 4200/s; east-1 fine |
| GC log | Young pauses 188–640 ms after 21:50 UTC; heap after GC still small; old ~228 MB |
| Histogram | `[C]` / `String` dominate; `IdempotencyRecord` ~1k; turnover, not 802’s million-record retain |

A worksheet that says only “excessive GC” or “leak” without allocation-versus-retained and without the DEBUG change scores poorly on Diagnostic method even if the lab title matches.

## Comms (acceptable example)

SEV-2 on create latency, `pay-prod-east-2` only. G1 pauses hundreds of milliseconds while allocation is about 1.8 GB/s. Old generation is not climbing. We are reverting the DEBUG overlay used to trace Avery. `pay-prod-east-1` still completing at normal pause times. Next update 20 minutes.
