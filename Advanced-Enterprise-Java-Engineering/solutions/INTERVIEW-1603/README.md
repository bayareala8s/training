# INTERVIEW-1603 — Instructor solution

**Do not share this file with students before Gate 1 quotes exist.**

This folder is **method shape**, not a hidden RCA. Do **not** lecture or require instructor RCAs from INCIDENT-1301, INCIDENT-1402, INCIDENT-1104, or INCIDENT-1205. Lucky title-match **must not** max Diagnostic method.

Symptom briefs are visible: `labs/INTERVIEW-1603/starter/symptom-https.txt` and `symptom-p99.txt`.

## Class A — HTTPS fail / tasks healthy (acceptable method)

**Gate 1 quotes (required).** Harbor cannot complete HTTPS to `payments.apps.baypay.example`. Tasks `RUNNING` 2/2. Jump-box HTTP `:8080` liveness **200**. Leftover `dmgr-east` **out of path**. Cert/ACM/DNS files **omitted**. Avery `11111111-…1111` / `c1603c33-…1603` never got a 201.

**Hypotheses (unproven).** Examples — students may name others:

- H1 unproven: merchant TLS/handshake class (leaf, SNI, protocol) vs working task HTTP.
- H2 unproven: DNS/name class for the teaching host.
- H3 withdrawn: bounce `dmgr-east` / PaymentCluster (brief says leftover, out of path).

None `proven`. Do not invent a cert dump so H1 can close.

**Next gate.** Request an **evidence class** (handshake / leaf / SNI / protocol / DNS) — not `aws acm` apply, not TLS-off, not “it’s INCIDENT-1402.”

**Stabilize / comms.** Do not disable TLS. Do not bounce ND or Postgres. HTTP `:8080` ≠ merchant HTTPS. Next update 20 minutes.

## Class B — P99 up / rate down (acceptable method)

**Gate 1 quotes (required).** Rate **~180→~22**. P99 **~118 ms→~4.8 s**. 5xx quiet. Hikari pending **0**. Scrape/tag files **omitted**. Late 201 for Avery / `c1603c33-…`.

**Hypotheses (unproven).**

- H1 unproven: saturation or wait **not** shown as 5xx (queue, lock, downstream, label/scrape class).
- H2 withdrawn or weakened: “the database is down” (pending **0**, no DB file).
- H3 withdrawn: bounce `dmgr-east`.

**Next gate.** Request the next **omitted kind** (scrape health / series count / meter tag names / deploy diff) — not a bounce, not “it’s INCIDENT-1301 cardinality.”

**Stabilize / comms.** Do not bounce Postgres. Do not announce a proven DB outage. Hold/rollback language is fine if marked unproven. Next update 20 minutes.

## Lucky RCA rule

A student who writes only “expired cert” or “high-cardinality labels” **without** Gate 1 quotes and **without** a next evidence class:

- may receive partial Technical accuracy if the class is plausible,
- **must not** receive 5 on Diagnostic method (20% weight).

Opening `solutions/INCIDENT-1301/`, `…1402/`, `…1104/`, or `…1205/` and reading the instructor story into the interview is a Diagnostic method **1**.

## Scoring notes

No AWS apply, no Bedrock, no portal, no TLS-off. Bank ids (AEJE-IQ-080 / 087) are optional color only.

## Comms (acceptable example)

SEV-2 interview method. Class A: HTTPS fail, tasks RUNNING, :8080 200. We are not bouncing dmgr-east and we are not turning TLS off. Next gate is handshake/SNI/leaf evidence — files are omitted on purpose. Avery’s client has no 201. Next update 20 minutes.
