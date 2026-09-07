# INC-K8S-1004 student worksheet

Fill in order. Quote evidence. Do not paste instructor solutions. Never write a live password.

**Incident:** Payment start failures after Secret update  
**Namespace:** `baypay-prod`  
**Your name / cohort:**  
**Time started:** 2026-09-06  
**Time submitted:** 2026-09-06  

## Current hypothesis

(What do you think is happening? Update after each gate.)

Gate 1: Secret `baypay-db` **exists**. Keys are `BAYPAY_DB_USER` and **`password`** (values `***`). CLUSTER contract is `BAYPAY_DB_USER` + **`BAYPAY_DB_PASSWORD`**. Sam’s BAYPAY-10044 “simplified to match the generic Postgres chart” dropped/renamed the process key. Existence ≠ contract. Next: logs — did the pod fail to create (`CreateContainerConfigError` / missing key) or **start** with an empty `BAYPAY_DB_PASSWORD` (auth / fail-fast bind)? Then Deployment env: `env.name` vs `secretKeyRef.key` and whether `optional: true`.

Gate 2: JVM **started** (not CreateContainerConfigError). `spring.datasource.password is empty; BAYPAY_DB_PASSWORD was not bound`. Hikari then `FATAL: password authentication failed for user "baypay_app"`. ApplicationContext fail-fast. Secret object exists; the **process env name** is empty. Not INC-1001 (URL) and not a stolen/rotated DB password — auth failed because the password string is **blank**. Question for gate 3: does Deployment `env.name=BAYPAY_DB_PASSWORD` still `secretKeyRef.key=BAYPAY_DB_PASSWORD` (key gone) with **`optional: true`** (empty instead of blocked pod)? Contrast `env.name` vs `secretKeyRef.key` vs Secret keys `password` / `BAYPAY_DB_USER`.

Gate 3: Yes.

| Process `env.name` | `secretKeyRef.key` | Secret keys present | `optional` |
|---|---|---|---|
| `BAYPAY_DB_USER` | `BAYPAY_DB_USER` | `BAYPAY_DB_USER` | (default false) |
| `BAYPAY_DB_PASSWORD` | `BAYPAY_DB_PASSWORD` | **`password` only** | **true** |

Missing `BAYPAY_DB_PASSWORD` key does not block the pod. Process starts with a blank password; Hikari auth-fails; Exit 1. RCA is **injection mapping**, not Postgres rotation.

## Supporting evidence

(File, timestamp, quote. Secret **key names**, log line, env.name vs secretKeyRef.key. Values as ***.)

- `timeline.json` 20:35Z Sam: re-applied `baypay-db` (BAYPAY-10044) “simplified to match the generic Postgres chart.” 20:58Z Priya: Running then datasource errors; Secret **keys only** — no decoded values in Slack. 21:18Z pager. 21:19Z Avery `c1004d44-…-111004` failed; same Idempotency-Key. 21:21Z Riley: no password in the bridge; do not bounce db-east.
- Gate 1 `evidence/secret-keys.txt`: keys `BAYPAY_DB_USER`, `password`; values `***`; ticket BAYPAY-10044. CLUSTER lists `BAYPAY_DB_PASSWORD`.
- Gate 2 `evidence/logs.txt` 21:02:16Z: `spring.datasource.password is empty; BAYPAY_DB_PASSWORD was not bound` then `FATAL: password authentication failed for user "baypay_app"`. ApplicationContext failed. Avery never AUTHORIZED.
- Gate 3 `evidence/deployment-env.yaml`: `name: BAYPAY_DB_PASSWORD` → `secretKeyRef.key: BAYPAY_DB_PASSWORD` **`optional: true`**.

## Next investigation

(What would you open or measure next, and why? If you wanted an omitted evidence kind, say what it would show.)

After gate 1: logs (gate 2) — CreateContainerConfigError vs started-with-empty-password. After gate 2: Deployment env (gate 3) — `env.name` vs `secretKeyRef.key` vs optional. Omitted full Secret `.data`: never request; values stay `***`. DB metrics would show auth failures from an empty password, not a role rotation — do not bounce. Do not invent a password.

## Stabilization action

(What restores the env contract *now*? Key versus mapping? What do you explicitly not do?)

Restore the **CLUSTER key** on Secret `baypay-db`: add `BAYPAY_DB_PASSWORD` (value from the vault / last known good — written as `***` here) **or** map `secretKeyRef.key` to `password` only if that key already holds the real secret. Prefer adding `BAYPAY_DB_PASSWORD` so the Deployment contract does not follow a generic chart. Set **`optional: false`** so a missing key is `CreateContainerConfigError`, not a blank password. Rolling-restart so pods remount. Do **not** bounce Postgres / db-east. Do **not** paste or commit a password (`changeme` in git fails this lab). Do **not** “rotate the DB role” as the first move.

## Remediation

(What remains after the page is quiet?)

Kyverno or a CI contract test: `baypay-db` **must** contain `BAYPAY_DB_PASSWORD` (and `BAYPAY_DB_USER`); apply fails otherwise. A human checklist lost to BAYPAY-10044. Keep **fail-fast on empty password** (better than a running pod that 500s). Prefer explicit `env.valueFrom` over `envFrom` for secrets so chart key names cannot silently collide. `optional: true` on a required password is a blast radius, not a convenience. Never commit real secrets; course placeholders stay `${}` / `***`.

## Communication update

(Five lines max. Audience: merchant success + platform lead. No unsupported cause. No password.)

SEV-2 `baypay-prod` / `payment-service` after the Secret window. Harbor Market / Avery `c1004d44-…-111004` never AUTHORIZED; same Idempotency-Key.  
Pods start, then fail-fast: `BAYPAY_DB_PASSWORD` **empty** → Postgres auth failed for `baypay_app`. Not CreateContainerConfigError.  
Sam’s BAYPAY-10044 left Secret keys `BAYPAY_DB_USER` + `password`. Deployment still refs key `BAYPAY_DB_PASSWORD` with **optional: true**.  
Restoring the CLUSTER key (or the mapping) and setting optional false. Values stay out of Slack / git.  
Not bouncing db-east. Not treating this as a stolen or rotated password. Next update when a replica binds and stays Ready.
