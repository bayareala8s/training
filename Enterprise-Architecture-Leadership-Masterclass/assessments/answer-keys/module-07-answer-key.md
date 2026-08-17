# Answer Key — Module 07 Quiz (Instructor Only)

**Do not distribute to students.**

| Q | Answer | Explanation | LO | Difficulty |
| - | ------ | ----------- | -- | ---------- |
| 1 | B | Zero Trust is posture across boundaries, not “delete VPN today.” | M07-LO1 | Easy |
| 2 | B | Data-plane boundary enforced by IAM scope + KMS policy | M07-LO1 | Medium |
| 3 | B | CRR helps region loss; versioning+drill is cheaper but weaker on region impairment | M07-LO3 | Medium |
| 4 | C | Logging/evidence primarily supports non-repudiation | M07-LO2 | Medium |
| 5 | B | Compliance conversations need residual risk + evidence freshness | M07-LO4 | Medium |
| 6 | B | RPO is data-loss tolerance in time | M07-LO3 | Easy |
| 7 | A | Overbroad read increases disclosure | M07-LO2 | Medium |
| 8 | B | Unfunded RTO is a leadership negotiation, not a silent promise | M07-LO3 | Hard |
| 9 | C | Shared admin role collapses least privilege | M07-LO1 | Hard |
| 10 | C | Time-bound exceptions with compensating controls | M07-LO4 | Medium |

## Scenario guidance

**S1:** Primary issues: Information disclosure + Elevation. Split contractor roles; prefix IAM; remove power-user; keep KMS. Residual: insider misuse within allowed prefix.

**S2:** Phase 1 versioning+drill+alarms; Phase 2 CRR if funded; do not promise RPO0/RTO30 without ops staffing and pattern funding.

**S3:** Drill runbook, timestamps, restored object evidence, alarm config, matrix row, owner, quarterly cadence.

## Discussion facilitation

**D1:** EA owns boundary design, ADRs, evidence architecture; CISO owns policy/risk appetite; avoid duplicate control implementation ownership.

**D2:** Simulated DR is honest for many Tier-1/2 cases when drills are real; insufficient when business impact requires geographic redundancy and funded failover.
