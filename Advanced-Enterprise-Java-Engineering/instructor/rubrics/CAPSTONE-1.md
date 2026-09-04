# Rubric — CAPSTONE-1 Build BayPay

**Type:** CAPSTONE  
**After:** Modules 1–3  
**awsLab:** no  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

Score each dimension 0–100, then apply the weight. A lucky curl of GET-by-id without a customer list is not a high Technical score. Opening `solutions/CAPSTONE-1/` before a student-authored list test caps Diagnostic method.

| Dimension | Weight | 100 | 60 | 20 |
|---|---|---|---|---|
| Technical accuracy | 25% | `./mvnw test` green; `GET ?customerId=` `200` array for Avery; missing query `400`; unknown customer `404 CUSTOMER_NOT_FOUND`; POST matrix intact (`201` / `200` / `409` / `400` / `422`); GET by id unchanged | List works; one miss (sort, `[]` vs `404`, or OpenAPI) | No list, or POST replay/`Idempotency-Key` broken |
| Diagnostic method | 20% | Proved existing `./mvnw test`, named the controller gap, wrote list tests that would fail without the method | Coded the list then added one happy-path test | Opened `solutions/` first or only used GET-by-id |
| Production awareness | 15% | Newest-first; known-empty `200 []`; AEJE-D-071 cited as ND **not** rebuilt; correlation still echoed | List present; ND mentioned as if they implemented it | New ear on `PaymentCluster` or second Boot app |
| Trade-off analysis | 15% | Defends required query vs nested `/customers/{id}/payments`; pagination out of scope; write-only idempotency | Preference with little why | No trade-off |
| Security / reliability | 10% | POST still requires `Idempotency-Key`; no PAN/CVV/body dump in logs; no unfiltered list | Key present; one debug `log` of the JSON body | Skips key or logs PAN |
| Communication | 10% | PF-service.md readable in five minutes; excerpt of list + IT names | Incomplete worksheet | Empty PF-service.md |
| Efficiency | 5% | Worked in `reference-apps/baypay/` with `JAVA_HOME` + `./mvnw` inside 4–8 hours | Finished; unused second module | New Spring Initializr app or required AWS/ND |

**Automatic caps**

- Missing `GET /api/v1/payments?customerId=` caps Technical accuracy at 20.
- Replay `201` or POST without `Idempotency-Key` caps Technical accuracy and Security / reliability at 20.
- PAN, CVV, or raw create-body logging fails Security / reliability even if tests are green.
- Recommending a new traditional ND cell or implementing the list as `payment.ear` on `PaymentCluster` caps Production awareness at 20.
- Setting `-Xmx` equal to a container / cgroup limit as “the way we run this” caps Production awareness at 60 (this capstone is a laptop JVM; still mark the error).

**Pass guideline:** weighted score ≥ 70, `./mvnw test` green, list-by-customer present with Bean Validation (or equivalent `400` on missing query), POST idempotency intact, no PAN in logs, PF-service.md filled. Live `spring-boot:run` neither raises nor lowers the score.
