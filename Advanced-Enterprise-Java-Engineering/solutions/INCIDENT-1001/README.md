# INCIDENT-1001 — Instructor solution

**Do not share this file with students before they submit a worksheet.**

## RCA

Sam Okada rolled ConfigMap `payment-config` in `baypay-prod` (BAYPAY-10011) and **dropped `BAYPAY_DB_URL`**. The Deployment still mounts that ConfigMap. Prod profile fail-fasts on an empty URL (no localhost default). Spring Boot bind / ApplicationContext fails. The container exits **1**. kubelet **CrashLoopBackOff**. Image pull succeeded; this is not ImagePullBackOff.

`kubectl logs` show `Failed to bind properties under 'spring.datasource.url'` and `ApplicationContextException`. The ConfigMap excerpt lists `SPRING_PROFILES_ACTIVE`, `BAYPAY_DB_USER`, `BAYPAY_LOG_LEVEL`, `JAVA_TOOL_OPTIONS` — not `BAYPAY_DB_URL`. Secret `baypay-db` is present. Postgres was not bounced.

This is not INCIDENT-1002 (Exit 137 / OOMKilled) and not INCIDENT-1004 (password key).

## Stabilization

1. **Restore** `BAYPAY_DB_URL` on ConfigMap `payment-config` **or revert** the Deployment / ConfigMap revision that dropped it.
2. Wait for Ready 3/3. Do not roll a new image first.
3. Do **not** bounce Postgres.
4. Do not bounce `dmgr-east`.
5. Do not bake the JDBC URL into the image to “avoid ConfigMap.”
6. Do not raise memory or change probes — Exit 1 after six seconds is startup bind.

## Remediation

- Treat `BAYPAY_DB_URL` as **required** in schema / policy. Do **not** ship an optional URL with a localhost default in prod.
- Contract-test rendered env (boot the JAR with the ConfigMap keys) before apply.
- Keep `BAYPAY_DB_*` out of the image.
- Optional: Kyverno / OPA that `payment-config` must contain `BAYPAY_DB_URL`.

## Evidence students should have used

| Gate | What it shows |
|---|---|
| describe.txt | CrashLoopBackOff; Last State Error; Exit 1; image pulled; env from `payment-config`; Ready 0 |
| logs.txt | Binding / ApplicationContext; `spring.datasource.url` empty; `BAYPAY_DB_URL` not set |
| configmap.yaml | Keys after the roll; `BAYPAY_DB_URL` absent |

A worksheet that says only “CrashLoop” without Exit 1 plus bind plus the missing key scores poorly on Diagnostic method even if the lab title matches.

## Comms (acceptable example)

SEV-2 on `payment-service` in `baypay-prod`. Pods CrashLoopBackOff with Exit 1 after the ConfigMap roll. Spring failed to bind the datasource URL. We are restoring the ConfigMap key or reverting that revision. Postgres is not being bounced. Next update 20 minutes.
