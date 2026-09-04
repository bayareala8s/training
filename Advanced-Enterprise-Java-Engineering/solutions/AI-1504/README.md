# AI-1504 — Instructor solution

**Do not share this file with students before they submit the worksheet and PF-ai.md quotes.**

The planted file [infrastructure/bayops-ai/fixtures/ai-1504-hallucination.json](../../infrastructure/bayops-ai/fixtures/ai-1504-hallucination.json) is **visible to students**. It is the artifact to evaluate, not a hidden RCA of INCIDENT-1104 or any other lab.

## Which claims are fabricated

Students must catch **all four**. Lucky “the AI is wrong” without quotes of (1) and (2) must **not** max Diagnostic method.

| # | Planted claim | Why it is fabricated | Student must quote |
|---|---|---|---|
| 1 | Citation `evidence/db-failover.json` | **That file does not exist.** Inventory says `NOT IN THIS PACK`. Database metrics were omitted. | The `source` field **and** the inventory / directory line |
| 2 | `provenRootCause`: **Postgres Multi-AZ writer failover in us-west-2 at 14:02** | Forbidden field (must be null/absent). Hypothesis marked `proven`. Tasks were RUNNING before and after 21:02 UTC. No RDS attached. | The `provenRootCause` string (or the proven hypothesis) |
| 3 | Bounce **`dmgr-east` / recycle PaymentCluster** | Leftover ND is **not on the merchant path**. `ecs-tasks.txt` does not list the cell. Timeline: Morgan offered, Priya/Riley refused. | The remediation action **and** a pack line that the cell is out of path |
| 4 | `humanApproval` **approved** by **BayOps-auto** | Auto-approve is a failed lab. A named human must reject. | `status: approved` / `by: BayOps-auto` |

Optional extras (score Communication if present): `approvalRequired: false`; “None. RCA is proven”; bounce the Postgres writer.

## What the pack actually shows

ALB / health **symptom class** only:

- ECS/Fargate `payment-service` tasks **RUNNING** 2/2, started ~18:40 UTC, no stop at 14:02 Pacific.
- ALB **502/503** (503 HTML from `awselb`, clients also 502).
- Target health **unhealthy**, healthy host count **0**.
- **No** database metrics file.
- Leftover cell is **not** in the describe.

Do **not** require students to name INC-AWS-1104’s `Path=/` RCA. If they independently guess a health-path miss, keep it **unproven**.

## Good rewrite

See [output.json](output.json).

- Evidence quotes inventory, ecs-tasks, alb-and-targets, and the planted dump **as the object under test**.
- H1 unproven (ALB/health vs RUNNING).
- H2 withdrawn (failover).
- H3 withdrawn (ND bounce).
- Investigation stays in ALB/health; do not invent the missing file.
- Remediation: reject planted mutates; no DB bounce; no `dmgr-east`; no TLS-off; `approvalRequired: true`.
- `humanApproval.status` = **`rejected`**.
- `provenRootCause`: `null`.

## Stabilization / remediation

1. **Reject** approval of the planted runbook.
2. Do **not** bounce Postgres or force another failover.
3. Do **not** bounce `dmgr-east` or recycle PaymentCluster.
4. Do **not** disable TLS.
5. Rewrite into four buckets. Mark hypotheses unproven / withdrawn.
6. Any later mutate that restores healthy targets still needs a **named** human.

## Comms (acceptable example)

SEV-2 evaluation. BayOps claimed a proven Postgres Multi-AZ failover at 14:02 and cited evidence/db-failover.json. That file is not in the pack. Tasks are RUNNING; ALB returns 502/503; targets unhealthy. We reject the auto-approve. We are not bouncing the database or dmgr-east. Next: ALB/health investigation only. Next update 20 minutes.

## Diagram

AEJE-D-070: missing citation + proven field + auto-approve → reject; rewrite four buckets.
