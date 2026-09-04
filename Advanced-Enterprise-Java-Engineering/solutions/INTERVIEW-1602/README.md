# INTERVIEW-1602 — Instructor solution

**Do not share this file with students before they log ten short answers.**

Rapid fire grades **coverage and tempo**, not Staff-depth and not PF-design. Sample landings below are **length and shape**. Students must use real ids from `simulator.py --mode rapid-fire --count 10`.

Do not require reveal first. Do not require a portal or Bedrock. Do not apply AWS.

## What “done” looks like

- Command: `python3 interview-bank/simulator.py --mode rapid-fire --count 10` (optional `--seed 16`).
- Ten rows: id, domain, ~60–90 seconds / 4–8 sentences, `ok` / `thin` / `froze`.
- Each landing: mechanism + BayPay name + one refusal or next check.
- Avery / `c1602b22-0000-4000-8000-111111111602` / `POST /api/v1/payments` at least once in the set.
- Reveal only **after** ten. Do not paste bank answers into the log as spoken.

## Acceptable landing shape (generic)

“On BayPay, `POST /api/v1/payments` for Avery Chen still hits `payment-service` on `:8080`. The thing I would name first is ___. I would not bounce `dmgr-east` / disable TLS / apply EKS / put `customerId` on a Micrometer label. Next check if we leave rapid fire: ___.”

That shape plus a stem-specific noun is enough. A 400-word Principal essay on item 1 and blanks on 8–10 fails Efficiency.

## What not to grade as depth

- Full 99.99% failure-domain table (that is INTERVIEW-1604).
- Full gated RCA (that is INTERVIEW-1603).
- Reciting INCIDENT-1301 / 1402 / 1104 / 1205 instructor titles.

## Scoring notes

`--count` other than 10 without a documented retake caps the mode contract. Reveal-as-you-go caps Diagnostic method. Two perfect essays and eight empty rows cap Efficiency at 1. Applying ACM because a TLS id appeared caps Production awareness.

## Comms (acceptable example)

Rapid fire, ten ids, seed optional. I landed short. I froze on one HA item and said so. I did not whiteboard. Avery’s create named once. No portal, no apply.
