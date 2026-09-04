# Capstones — BayPay Enterprise Delivery

**Case study:** BayPay Financial Services (fictional)  
**Portal section:** Capstones: BayPay Enterprise Delivery  
**After:** Modules 1–16 (each capstone lists the modules it assumes)

These four capstones are the course’s **delivery**, not extra trivia. You synthesize the BayPay reference app, the leftover `BayPayCell`, containers, AWS (paper + `terraform validate`), and a progressive SEV-1. Instructor solutions live under `solutions/CAPSTONE-N/`. Do not open them first on CAPSTONE-4.

| Id | Title | After | Type | Cost |
|---|---|---|---|---|
| [CAPSTONE-1](01-build-baypay/README.md) | Build BayPay | Modules 1–3 | Java quality bar + list-by-customer | $0 |
| [CAPSTONE-2](02-modernize-baypay/README.md) | Modernize BayPay | Modules 4–10 | ND → Liberty → containers → K8s/OCP paper | $0 |
| [CAPSTONE-3](03-cloud-baypay/README.md) | Cloud BayPay | Modules 11–12 | AWS Fargate design; `validate` bar | $0 unless you apply |
| [CAPSTONE-4](04-production-crisis/README.md) | BayPay Production Crisis | Modules 13–15 | Progressive SEV-1 (`INC-CAP-4`) | $0 |

Diagrams: **AEJE-D-071** (initial WebSphere topology) and **AEJE-D-072** (cloud-native target). Locked names: [TOPOLOGY.md](../datasets/baypay-cell/TOPOLOGY.md), [ACCOUNT.md](../datasets/baypay-aws/ACCOUNT.md), [OBSERVABILITY.md](../datasets/baypay-ops/OBSERVABILITY.md), [BAYOPS.md](../datasets/baypay-ai/BAYOPS.md).

Time-box 4–8 hours each. CAPSTONE-4 is 90–150 minutes of gated diagnosis. Traditional ND is the **source estate**. Do not apply NAT, EKS, or RDS Multi-AZ. Do not bounce `dmgr-east` as a cloud stabilize.

Portfolio: `PF-service.md`, `PF-modernize.md`, `PF-cloud.md`, `PF-crisis.md`.

**PAKS is optional.** Capstones reuse the module deep dives listed in [PAKS_LINKS.md](../PAKS_LINKS.md). No extra PAKS chapter is required.
