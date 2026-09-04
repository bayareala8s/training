# INCIDENT-1004 — Instructor solution

**Do not share this file with students before they submit a worksheet.**

## RCA

Secret `baypay-db` has keys `BAYPAY_DB_USER` and **`password`** (generic chart naming). It does **not** have `BAYPAY_DB_PASSWORD`. The Deployment env **name** is `BAYPAY_DB_PASSWORD` with `secretKeyRef.key: BAYPAY_DB_PASSWORD` and **`optional: true`**. The pod starts. The process receives an **empty** password. Hikari fail-fast: Postgres `password authentication failed for user "baypay_app"` and ApplicationContext fails.

This is an injection-name miss, not a stolen credential and not a down database. CLUSTER.md contract is keys `BAYPAY_DB_USER`, `BAYPAY_DB_PASSWORD`. Do not write a live password into notes.

This is not INCIDENT-1001 (`BAYPAY_DB_URL` missing from ConfigMap).

## Stabilization

1. **Add** key `BAYPAY_DB_PASSWORD` to Secret `baypay-db` (value from the secret store, not git) **or** map `env.valueFrom.secretKeyRef.key` to the key that exists (`password`) **and** keep the process env name `BAYPAY_DB_PASSWORD`.
2. Remove `optional: true` so a missing key blocks the pod instead of starting blank.
3. Do **not** bounce Postgres to “refresh” the role.
4. Do not bounce `dmgr-east`.
5. Do not commit a real secret or a `changeme` that someone might reuse.
6. Do not paste values into Slack. Keys only.

## Remediation

- Contract test or **Kyverno**: `baypay-db` must contain `BAYPAY_DB_PASSWORD`; Deployment must reference that key.
- **Never commit real secrets.** Teaching files use `${BAYPAY_DB_PASSWORD}` / `***` only.
- Prefer explicit `env.valueFrom` over chart `envFrom` that injects `password` as the env name.
- App fail-fast on empty `BAYPAY_DB_PASSWORD` is correct; keep it.

## Evidence students should have used

| Gate | What it shows |
|---|---|
| secret-keys.txt | Keys `BAYPAY_DB_USER`, `password`; values `***`; no `BAYPAY_DB_PASSWORD` |
| logs.txt | Empty `spring.datasource.password`; auth failed `baypay_app`; ApplicationContext fail-fast |
| deployment-env.yaml | env name `BAYPAY_DB_PASSWORD`; key `BAYPAY_DB_PASSWORD`; `optional: true` |

A worksheet that says only “bad Secret” without env name versus key names scores poorly on Diagnostic method even if the lab title matches. A fabricated password fails Security.

## Comms (acceptable example)

SEV-2 on `payment-service` after the `baypay-db` Secret change. The process env name and the Secret key names do not match, so the password is empty. We are adding the correct key or fixing the mapping. We are not rotating the database role and we are not posting secret values. Next update 20 minutes.
