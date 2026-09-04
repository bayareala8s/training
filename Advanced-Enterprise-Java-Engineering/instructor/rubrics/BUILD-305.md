# Rubric — BUILD-305 Health and readiness endpoints

Score each dimension 0–100, then apply the weight. `include: '*'` at handoff caps Security even if `HealthApiIT` is green.

| Dimension | Weight | 100 | 60 | 20 |
|---|---|---|---|---|
| Technical accuracy | 25% | `HealthApiIT` green; liveness + readiness `200`; probes enabled; allow-list `health,info,metrics` | Health `UP`; probes 404 or extra endpoints | No Actuator / wrong process |
| Diagnostic method | 20% | Used probe 404/`DOWN` logs to find `probes.enabled` or datasource | YAML edits until curl worked | Copied Boot docs blindly |
| Production awareness | 15% | Policy: DB blip is readiness, not liveness; local details vs prod `never` | Mentions probes; no policy | One `/health` for everything |
| Trade-off analysis | 15% | Management port, `db` vs `select 1`, extract implications | One preference | No trade-off |
| Security / reliability | 10% | Heapdump/env/shutdown off; cheap probes; prod details hidden | Allow-list correct; details always | `include: '*'` or heapdump `200` |
| Communication | 10% | Four-line BayPay-specific probe policy | Generic Boot paraphrase | Empty |
| Efficiency | 5% | Configured `payment-service` | Finished | Second “ops” app |

**Pass guideline:** weighted score ≥ 70 and heapdump is not exposed on port 8080.
