# AI-1502 — Instructor solution

**Do not share this file with students before they submit `output.json`.**

## What the starter got wrong

`labs/AI-1502/starter/hypotheses.json` has **too few** hypotheses, marks the only one **`proven`**, and only wants to **bounce `dmgr-east` / PaymentCluster**. It auto-approves. That fails the contract.

The excerpt is the INC-SEC-1402 **symptom class**: merchant HTTPS fails, tasks **RUNNING**, HTTP `:8080` **200**. It does **not** include ACM describe or Route 53. Students must not be handed `PENDING_VALIDATION` or a deleted validation CNAME as the answer in the student lab.

## Good output

See [output.json](output.json).

| Bucket | Must include |
|---|---|
| Evidence | Handshake / `curl: (60)` / expired `notAfter` **quoted**; RUNNING 2/2; `:8080` 200; omitted ACM/DNS/DB/cell files named as omitted. |
| Hypotheses | ≥3. All `unproven` / `weakened` / `withdrawn`. Edge/handshake **unproven**. App-down **withdrawn**. Cell bounce **withdrawn**. Database **withdrawn**. |
| Recommended investigation | Next files in the **cert / ACM / DNS** class. Not a mutate. Not “RCA is proven.” |
| Suggested remediation | Restore HTTPS, `approvalRequired: true`. No TLS-off. No ND bounce. No Postgres bounce. |
| humanApproval | `pending` (or named reject of the cell bounce). |
| provenRootCause | omitted or `null` |

## Lucky “cert expired”

The excerpt contains `certificate has expired`. A student may quote that. They must still leave the hypothesis **unproven** and name ACM/DNS as **next** investigation.

A lucky “cert expired” marked **proven** with no quotes (or with no next investigation) must **not** max Diagnostic method — same spirit as INCIDENT-1402, but this lab does **not** require the validation-CNAME story to pass.

Do **not** put `PENDING_VALIDATION` or `_2f91d4c0` in the student README. If a student independently opens INC-SEC-1402 gates after writing hypotheses, they may add quotes; they still must not stamp proven RCA on the AI-1502 output.

## Stabilization

Restore HTTPS. Do not disable TLS. Do not bounce `dmgr-east`. Do not bounce Postgres. Do not bounce healthy tasks.

## Comms (acceptable example)

SEV-2 on payments.apps.baypay.example. Merchants fail the TLS handshake. Tasks remain RUNNING and HTTP on :8080 answers. Next check is the certificate at the edge and DNS/ACM paper describe. Not bouncing the leftover cell or the database. No proven RCA. Next update 20 minutes.

## Diagram

AEJE-D-068: quoted handshake ≠ proven RCA.
