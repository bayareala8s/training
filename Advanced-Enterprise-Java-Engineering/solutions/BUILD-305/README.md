# Solution — BUILD-305 Health and readiness endpoints

Instructor only.

## Target configuration

`reference-apps/baypay/payment-service/src/main/resources/application.yml`:

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics
  endpoint:
    health:
      probes:
        enabled: true
      show-details: when_authorized
  health:
    livenessstate:
      enabled: true
    readinessstate:
      enabled: true
```

`application-local.yml`: `management.endpoint.health.show-details: always`.  
`application-prod.yml`: `show-details: never`.

`HealthApiIT` asserts `/actuator/health` is `UP` and liveness/readiness return `200`.

## Probe policy (acceptable student wording)

- **Liveness:** restart the JVM only if it cannot make progress. Do not tie this to a 30-second PostgreSQL blip.
- **Readiness:** stop sending `POST /api/v1/payments` when the DataSource (or equivalent) cannot serve.
- **Aggregated `/actuator/health`:** operator/platform document; may include `db`.
- **Exposure:** never `*`. `heapdump`, `env`, `shutdown`, `beans` stay off the payment port.

## Endpoints that must stay off the allow-list

`heapdump`, `threaddump` (unless a locked management port), `env`, `configprops`, `beans`, `shutdown`, `logfile`.

## Validation command

```bash
cd reference-apps/baypay
./mvnw -pl payment-service -am -Dtest=HealthApiIT test
curl -sS -o /dev/null -w '%{http_code}\n' http://localhost:8080/actuator/heapdump
```

Heapdump must not be `200`.

## Common gaps

| Symptom | Likely miss |
|---|---|
| `/liveness` 404 | `probes.enabled` false |
| Details in prod-profile run | no `show-details: never` |
| Heapdump `200` | `include: '*'` |
| Health used as both kube probes | policy note missing |

## Rubric notes

Technical accuracy: three URLs + allow-list. Production awareness: liveness versus readiness. Security: heapdump/env off. Communication: the four-line policy.
