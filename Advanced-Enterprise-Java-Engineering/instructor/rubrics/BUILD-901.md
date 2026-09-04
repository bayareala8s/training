# Rubric — BUILD-901 Containerize BayPay

**Type:** BUILD  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

Score each dimension 0–100, then apply the weight. Docker absence must not fail the lab. A single-stage JDK file is not a high Technical score.

| Dimension | Weight | 100 | 60 | 20 |
|---|---|---|---|---|
| Technical accuracy | 25% | Two stages; `./mvnw` package; runtime `eclipse-temurin:21-jre`; `EXPOSE 8080`; `USER 10001`; JAR via `COPY --from` | Multi-stage but JDK left as final `FROM`, or missing `EXPOSE` | Single-stage starter left unchanged |
| Diagnostic method | 20% | Listed starter gaps (JDK runtime, no `USER`, whole-tree copy) before editing | Edited until it “looked like” a blog Dockerfile | Opened `solutions/` first |
| Production awareness | 15% | Names `registry.baypay.example/baypay/payment-service`, Avery port 8080, `BAYPAY_DB_*` at runtime | Image works on paper; no production names | Treats the file as a local demo only |
| Trade-off analysis | 15% | Multi-stage vs laptop-built JAR; fat JAR vs exploded layers (deferred) | States a preference with little why | No trade-off |
| Security / reliability | 10% | `USER 10001`; no secret `ENV`; no `-Xmx` = limit | Non-root missing **or** a convenience password | Root plus a password layer |
| Communication | 10% | Checklist complete; PF-container image/user sections readable | Incomplete excerpt | Empty worksheet |
| Efficiency | 5% | Checklist only; no required engine | Finished in session | Built a paid registry or AWS pipeline as if required |

**Pass guideline:** weighted score ≥ 70, runtime is a JRE, `USER 10001` present, no secret values. Optional Docker neither raises nor lowers the score.
