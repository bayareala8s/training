# BUILD-305 — Probe policy

Date: 2026-09-06

Allow-list: `health,info,metrics`. Probes enabled. Details: base `when_authorized`, local `always`, prod `never`.

## Four lines

1. `GET /actuator/health/liveness` — is this JVM still a process we should keep? Restart only if this is DOWN. Do **not** put the DataSource here.
2. `GET /actuator/health/readiness` — may this instance take `POST /payments`? DOWN if the DB (or later the pool) cannot serve. Pull it from the load balancer.
3. `GET /actuator/health` — composite for humans. In prod, status only (`show-details: never`).
4. Never expose `heapdump`, `env`, `loggers`, or `include: '*'` on 8080.

## Interview

A DB blip is readiness, not liveness: killing the pod on every failover makes a brownout a restart storm. `include: '*'` puts heap and env on the payment port. Prod health should not leak datasource URLs; authenticate or hide details.
