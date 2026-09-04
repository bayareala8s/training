# AI-1503 — Instructor solution

**Do not share this file with students before they submit `output.json`.**

## What the unsafe starter got wrong

`labs/AI-1503/starter/runbook.json` does four things Priya Nair rejects on sight:

1. **Disable TLS** on the ALB listener to “restore HTTP.”
2. **Bounce `dmgr-east`** / recycle PaymentCluster (leftover ND, not on the Fargate path).
3. **Bounce Postgres** (no database metrics in the excerpt).
4. **Auto-approve** (`humanApproval.status=approved` by `BayOps-auto`, `approvalRequired: false`).

It also marks a hypothesis `proven`. That fails the contract.

## Good runbook

See [output.json](output.json).

| Bucket | Must include |
|---|---|
| Evidence | Handshake / expired leaf quoted; RUNNING; `:8080` 200; Riley/Morgan lines that TLS stays on and ND is out of path. |
| Hypotheses | Edge/HTTPS restore **unproven**. TLS-off, ND bounce, Postgres bounce **withdrawn**. |
| Recommended investigation | **Check cert / edge first** (describe leaf, listener, optional ACM/DNS paper). Non-mutating. |
| Suggested remediation | Restore HTTPS. Every item `approvalRequired: true`. Explicit refusals. |
| humanApproval | `pending` on the restore, and/or a named **reject** of the starter auto-approve. Not `BayOps-auto` approved. |
| provenRootCause | omitted or `null` |

`incidentId` may be `INC-AI-1503` or `INC-AI-1502` if the student treats it as the same page.

## Stabilization

Restore HTTPS. Do **not** disable TLS. Do **not** bounce `dmgr-east`. Do **not** bounce Postgres. Do not recycle PaymentCluster.

A runbook that only says “renew the cert” without a cert/edge **check** and without `approvalRequired: true` loses Diagnostic method / Production awareness.

## Comms (acceptable example)

SEV-2 runbook rewrite. Merchants fail HTTPS; tasks RUNNING; :8080 200. We will check the leaf and listener before any mutate. We will not turn TLS off, bounce dmgr-east, or bounce Postgres. humanApproval pending Riley or Priya. Next update 20 minutes.

## Diagram

AEJE-D-070: named human in front of mutate.
