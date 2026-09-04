# Rubric — PERFORMANCE-904 Optimize Java container

**Type:** PERFORMANCE  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

Score each dimension 0–100, then apply the weight. Docker absence must not fail the lab. `-Xmx` equal to the memory limit cannot score high on Technical or Production.

| Dimension | Weight | 100 | 60 | 20 |
|---|---|---|---|---|
| Technical accuracy | 25% | Poms copied before sources; JRE runtime; `JAVA_TOOL_OPTIONS` has `UseContainerSupport` and `MaxRAMPercentage` < 100 | Poms first **or** flags correct, not both | `-Xmx` equal to the limit, or JDK runtime |
| Diagnostic method | 20% | Explains why a Java-only edit should not re-download Maven plugins; shows flag rationale | Flags without COPY reasoning | Solution file only |
| Production awareness | 15% | Cites INCIDENT-806 / LAB-704; native headroom; CLUSTER.md | Mentions cache or heap, not both | “Use all the RAM” or a required cluster |
| Trade-off analysis | 15% | 75% vs lower when threads/direct grow; `%` vs explicit `-Xmx` with headroom; optional `jlink` named | One honest trade-off | None |
| Security / reliability | 10% | Headroom as reliability; still `USER 10001`; no secrets | Mentions headroom | Heap = limit as the strategy |
| Communication | 10% | PF-container JVM flags section with percentage and refusal | Flags without math | Empty |
| Efficiency | 5% | Paper path, `$0`; Docker extra only | Docker attempted, paper complete | EKS/minikube/jlink marathon as if required |

**Pass guideline:** weighted score ≥ 70, pom-before-source order visible, `MaxRAMPercentage` below 100, and `-Xmx` equal to the limit is rejected. Missing `jlink` is not a deduction.
