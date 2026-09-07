# INTERVIEW-1603 method notes

**Class:** A — HTTPS fail / tasks healthy  
**Brief:** `labs/INTERVIEW-1603/starter/symptom-https.txt`  
**When:** 2026-09-03 00:20 Pacific (07:20 UTC)  
**Did not open:** `solutions/INTERVIEW-1603/`, `solutions/INCIDENT-1301/`, `1402`, `1104`, `1205`.

Lucky-RCA trap: I have seen this **symptom class** before. I will **not** treat a prior lab title as proven here. Quotes + next gate only.

---

## Gate 1 — quotes from this brief

1. “Browser cannot complete HTTPS to the teaching host” (`payments.apps.baypay.example`).
2. “Merchant app retries; no 201; not a domain decline.”
3. Avery Chen `11111111-…-1111`, account `…221`; payment **`c1603c33-0000-4000-8000-111111111603`** “client never sent.”
4. Priya: ECS/Fargate tasks **`lastStatus: RUNNING`**, desired 2, running 2.
5. Jump box `http://<task-ip>:8080/actuator/health/liveness` → **200**.
6. Omitted: “No certificate dump. No ACM / Route 53 apply output.”
7. “Morgan named dmgr-east; Riley said it is **out of path**.”
8. Must not: bounce dmgr-east / PaymentCluster / Postgres; disable TLS; apply `aws acm` / `aws route53`.

**Coexistence:** RUNNING + `:8080` **200** while Harbor Market cannot handshake `:443`.

---

## Hypotheses (none proven)

| Id | Status | Statement |
|---|---|---|
| H1 | **unproven** | Edge / handshake / leaf / SNI problem on `payments.apps.baypay.example:443` — merchants never reach Spring. |
| H2 | **withdrawn** | `payment-service` is down. Contradicted: RUNNING 2/2 + liveness 200. |
| H3 | **withdrawn** | Bounce `dmgr-east` / PaymentCluster. Riley: leftover cell **out of path**. |
| H4 | **withdrawn** | Postgres writer is down. No DB metrics in the brief; handshake may never have reached JDBC. |
| H5 | **unproven** | DNS / name the client resolves ≠ the healthy tasks (protocol/DNS class). Omitted until a lookup file exists. |

---

## Gate 2 — next evidence class

Request **handshake / leaf / SNI** first (openssl/curl-class paste: verify error, `notAfter`, SNI, whether TCP completed). Then, if needed, **DNS** class (what name resolves). Why: RUNNING + `:8080` 200 already show the JVM; the merchant path is **HTTPS at the edge**. Do **not** invent a cert dump. Do **not** apply ACM/Route 53. Do **not** skip to bounce.

---

## Stabilize / comms (Priya, Riley, Harbor Market)

SEV-2 `payments.apps.baypay.example`: Harbor Market cannot complete HTTPS. Avery `c1603c33-…1603` never left the client — no 201, not a decline. Tasks **RUNNING 2/2**; jump-box `:8080` liveness **200** — we are **not** bouncing Postgres or `dmgr-east` and we are **not** turning TLS off. Next update in **20 minutes** after a handshake/leaf/SNI paste (not an apply). Hypothesis H1 stays **unproven** until that file exists.

---

## What I will not do

No TLS-off. No `dmgr-east` / PaymentCluster bounce. No Postgres bounce. No `aws acm` / `aws route53`. No invented cert file. No lecture of a prior instructor RCA as *this* answer.
