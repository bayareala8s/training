# AI-1501 — Instructor solution

**Do not share this file with students before they submit `output.json` and the PF-ai four-bucket section.**

## What the mixed starter got wrong

`infrastructure/bayops-ai/fixtures/ai-1501-mixed-summary.json` collapses a **throughput drop + P99 rise** excerpt into “the database is down,” sets `provenRootCause` to a string, marks a hypothesis `proven`, cites **`invented/db-down.txt`** (not on disk), auto-approves a bounce of Postgres and `dmgr-east`, and sets `approvalRequired: false`.

That fails the BayOps contract. The excerpt shows rate **~182 → ~22** RPS, P99 **~118 ms → ~4.82 s**, 5xx still ~0.05 RPS, Hikari pending **0**, servlet threads busy, and Avery’s payment `c1501d33-0000-4000-8000-111111111501` a **late 201**. It explicitly has **no** database metrics file.

## Good four-bucket rewrite

See [output.json](output.json). Required shape:

| Bucket | Must include |
|---|---|
| Evidence | Quotes from `labs/AI-1501/starter/evidence-excerpt.txt` only (rate, P99, 5xx-not-the-page, Hikari pending 0, omitted DB file). No `invented/db-down.txt`. |
| Hypotheses | Ranked. `unproven` / `weakened` / `withdrawn` only. “Database is down” is **withdrawn** (or weakened) because Hikari pending is 0 and no DB file shipped. |
| Recommended investigation | Next omitted kind (scrape/JVM if they have INC-PROD-1301) or last-healthy-image confirm. Not a bounce. |
| Suggested remediation | Stabilize without Postgres / `dmgr-east`. Every item `approvalRequired: true`. |
| humanApproval | `pending` (or a named reject of the mixed bounce). Not `BayOps-auto`. |
| provenRootCause | omitted or `null` |

Students may keep `humanApproval.pending` even if they personally would roll back to `3.8.4`. Signing the rollback is a later human act.

## What this solution must not do in the student lab

The **student** README and excerpt must not lecture the Module 13 instructor RCA (Micrometer `customerId` / `accountId` cardinality, series explosion, scrape timeout). If a student independently names those after opening INC-PROD-1301 gate 3, score Technical accuracy on whether they still kept hypotheses **unproven** and still quoted **this** excerpt’s rate/P99/Hikari lines. Do not require the cardinality story to pass AI-1501.

A lucky “database” or “just a bad deploy” with no quoted **rate**, **P99**, and **Hikari pending** must not max Diagnostic method.

## Stabilization / remediation (teaching)

1. Do **not** bounce Postgres or `dmgr-east`.
2. Do **not** announce a writer outage in comms.
3. Prefer hold / rollback to the last healthy image **named on the excerpt** if a human approves.
4. Next investigation is process/scrape work after 18:08, not a database file you invent.

## Comms (acceptable example)

SEV-2 on payment-service us-west-2. Completions ~180 to ~22 RPS; P99 ~4.8 s; 5xx not the page. Avery late 201 on c1501d33-…. Hikari pending 0; no database file in the excerpt. Mixed BayOps “database is down / proven” is withdrawn. Rollback to 3.8.4 is pending named approval. Not bouncing the database or dmgr-east.

## Diagram

AEJE-D-068: excerpt quotes → unproven hypotheses. AEJE-D-069: paper BayOps; human approval in front of mutate.
