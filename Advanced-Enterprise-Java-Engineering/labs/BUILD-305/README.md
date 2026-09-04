# BUILD-305 — Health and readiness endpoints

**Type:** BUILD  
**Module:** 3 — Spring Boot Engineering  
**Duration:** 60–90 minutes  
**Lessons:** [L-3.5](../../course/modules/03-spring-boot-engineering/lessons/L-3.5.md)

---

## Scenario

Platform engineering will put BayPay behind a load balancer and, later, Kubernetes. You configure Spring Boot Actuator on the existing `payment-service` process so liveness and readiness are real probe targets — not a homepage ping.

---

## Business context

If the JVM is alive but PostgreSQL is down, Avery Chen’s `POST /payments` must not land on that instance. If you expose `heapdump` on port 8080, compliance will fail the release. You configure `reference-apps/baypay/` only.

---

## Learning objectives

- Enable Actuator web exposure for `health`, `info`, and `metrics` only.
- Enable liveness and readiness group probes.
- Keep `show-details: always` in `local` and `never` in `prod`.
- Prove `/actuator/health`, `/actuator/health/liveness`, and `/actuator/health/readiness` with `HealthApiIT` and curl.
- Write a four-line probe policy: what each URL means for a payments process.

---

## Architecture

```text
Load balancer / kubelet
    ├── GET /actuator/health/liveness   (restart?)
    ├── GET /actuator/health/readiness  (traffic?)
    └── GET /api/v1/payments            (only if ready)
```

One process, one probe surface. Diagram: `AEJE-D-012`.

---

## Prerequisites

- L-3.5. Java 21. App boots on port 8080.

---

## Environment setup

```bash
export JAVA_HOME="${JAVA_HOME:-/opt/homebrew/opt/openjdk@21}"
cd reference-apps/baypay
./mvnw -pl payment-service -am spring-boot:run
```

Edit `payment-service/src/main/resources/application.yml` plus the `local` and `prod` profile files. Do not add a second Boot application for “ops.”

---

## Challenge / tasks

1. Confirm `management.endpoints.web.exposure.include` is the allow-list `health,info,metrics`.
2. Enable `management.endpoint.health.probes.enabled` and both `livenessstate` and `readinessstate`.
3. Set health details: local `always`, prod `never`, base `when_authorized`.
4. `GET /actuator/health` returns `{"status":"UP"}` (details optional by profile).
5. `GET /actuator/health/liveness` and `/readiness` return `200` when the app can serve.
6. Confirm `/actuator/heapdump` is **not** exposed (expect `404`).
7. Write the probe policy in your notes: liveness does not include “database down”; readiness does.

---

## Validation

```bash
cd reference-apps/baypay
./mvnw -pl payment-service -am -Dtest=HealthApiIT test
```

```bash
curl -sS http://localhost:8080/actuator/health
curl -sS http://localhost:8080/actuator/health/liveness
curl -sS http://localhost:8080/actuator/health/readiness
curl -sS -o /dev/null -w '%{http_code}\n' http://localhost:8080/actuator/heapdump
```

Heapdump must not be `200`.

---

## Troubleshooting

- Probe URLs 404: `probes.enabled` is false (Boot will not register group endpoints).
- Health is `DOWN` in test: H2 test datasource failed to start; read the boot log, not the JSON first.
- Details visible in a prod-profile run: `application-prod.yml` did not override `show-details`.
- `include: '*'` makes heapdump `200` — revert to the allow-list.

---

## Expected outcome

`HealthApiIT` green. Curl shows UP/200 on the three health URLs. Heapdump is not on the application port. You have a written liveness versus readiness policy for BayPay.

---

## Interview questions

1. Why is a database blip a readiness failure and not a liveness failure?
2. What is the risk of `include: '*'` on a payments JVM?
3. Should `/actuator/health` require an authenticated user in prod?

---

## Architecture/trade-off questions

1. Same port versus `management.server.port` for probes.
2. Default `db` indicator versus a custom `select 1` indicator.
3. When you extract `notification-service`, do probes split? What does the monolith still advertise?

---

## Cleanup

Stop the app. No cloud resources. Revert any `include: '*'` experiment.

---

## Cost estimate

**$0.**

---

## Hidden/revealable solution

Compare YAML and the policy wording with `solutions/BUILD-305/` after `HealthApiIT` has been run. The solution lists endpoints that must stay off the allow-list.

---

## What you learned

- Actuator is part of the BayPay process, not a sidecar tutorial app.
- Liveness and readiness answer different operator questions.
- Exposure is an allow-list for a reason.

---

## Portfolio deliverable

Attach the probe policy and the Actuator YAML excerpt to the Module 3 artifact. Capstone 1 reviewers should see that health was designed, not left on Boot defaults.
