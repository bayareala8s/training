# INCIDENT-1003 — Instructor solution

**Do not share this file with students before they submit a worksheet.**

## RCA

`readinessProbe` is `httpGet` path **`/actuator/health/readiness`**. The rolled image `3.9.1-slim` only exposes **`/actuator/health`**. That readiness path returns **404**. Pods stay **Running**, **Ready 0/1**. Service **Endpoints are empty**. Ingress returns **503**.

**Liveness** on `/actuator/health` still **passes** (HTTP 200), so kubelet does not restart the JVM. This is a BUILD-305 contract miss: probes must match Actuator **groups**, not the aggregate health URL alone.

This is not INCIDENT-1006 (selector vs labels; those pods are Ready). This is not a database-down readiness (404, not a `DOWN` body). Postgres was not the first object.

## Stabilization

1. **Fix the probe path** to a URL the image actually serves, **or add** the readiness group (`management.health.readinessstate` / probes from BUILD-305) and roll the image.
2. Prefer adding `/actuator/health/readiness` to the image so liveness and readiness stay distinct.
3. Do **not** bounce Postgres.
4. Do not bounce `dmgr-east`.
5. Do not delete the Ingress.
6. Do not use `/actuator/health` as both probes as a permanent design.

## Remediation

- Probes must match Actuator groups from **BUILD-305**: liveness `/actuator/health/liveness`, readiness `/actuator/health/readiness`.
- CI: curl probe paths against the image before the Deployment merges.
- Do not ship a “slim” cut that drops `probes.enabled` while YAML still names `/readiness`.
- Keep aggregate `/actuator/health` for operators; do not make it the only kubelet readiness target without documenting why.

## Evidence students should have used

| Gate | What it shows |
|---|---|
| describe.txt | Running; Ready 0/1; readiness 404 on `/actuator/health/readiness`; liveness 200 on `/actuator/health` |
| endpoints.txt | `subsets: []` / ENDPOINTS none |
| curl-ingress.txt | HTTP 503 after a completed TLS handshake |

A worksheet that says only “readiness” without quoting the 404 path versus the image health URL scores poorly on Diagnostic method even if the lab title matches.

## Comms (acceptable example)

SEV-2 on `payments.apps.baypay.example`. Pods are Running and not Ready. Readiness probe returns 404. Service Endpoints are empty, so Ingress is 503. We are fixing the probe path or restoring the readiness Actuator group. Database is not being bounced. Next update 20 minutes.
