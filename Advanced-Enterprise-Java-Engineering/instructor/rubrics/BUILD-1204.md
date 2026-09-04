# Rubric — BUILD-1204 CI/CD pipeline

**Type:** BUILD  
**awsLab:** no  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

Score each dimension 0–100, then apply the weight. GitHub-hosted runner absence must not fail the lab. A publish-only workflow is not a high Technical score.

| Dimension | Weight | 100 | 60 | 20 |
|---|---|---|---|---|
| Technical accuracy | 25% | Test job; Temurin/Java **21**; `./mvnw` `test`; publish `needs` test; tag `${{ github.sha }}` | Test job present; Java 17 or `mvn` without Wrapper | Starter unchanged (publish + `:latest` only) |
| Diagnostic method | 20% | Listed missing test job and `:latest` before editing | Edited until it resembled a blog workflow | Opened `solutions/` first |
| Production awareness | 15% | SHA tag is the deploy tag; tests on PR; AEJE-D-056; working-directory `reference-apps/baypay` | SHA present; still also deploys `:latest` as the only name ECS would use | `-DskipTests` labeled as the test job |
| Trade-off analysis | 15% | `needs` vs parallel; Actions vs generic CI; smoke deferred to 1205 | Preference with little why | No trade-off |
| Security / reliability | 10% | Secret **names** only; no key material | Secrets omitted; no keys | `AKIA` / password / `changeme` in YAML |
| Communication | 10% | PF-iac CI/CD section; jobs named in prose | Incomplete excerpt | Empty worksheet |
| Efficiency | 5% | YAML checklist only | Finished in session | Required paid runners or an ECS apply |

**Pass guideline:** weighted score ≥ 70, test job with Java 21 and Wrapper `test`, SHA tag, no secrets. Live Actions neither raises nor lowers the score.
