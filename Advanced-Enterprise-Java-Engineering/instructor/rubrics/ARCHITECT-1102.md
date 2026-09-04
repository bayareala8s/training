# Rubric — ARCHITECT-1102 ECS vs EKS vs OpenShift

**Type:** ARCHITECT  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

The compact pick in the student lab is a *post-attempt* hint. Using it as the first draft of `PF-aws-platform.md` without win/lose paragraphs caps Diagnostic method. A plan that applies EKS “for realism” must not outscore an ACCOUNT.md-based page.

| Dimension | 5 | 3 | 1 |
|---|---|---|---|
| Technical accuracy | Three columns; ECS is apply default; EKS and OpenShift have honest wins; mapping inset; health path same in every home | Columns present; one win thin | “Always EKS”; OpenShift marked legacy; invented fourth default |
| Diagnostic method | Expanded ACCOUNT.md + Module 10 objects after BUILD-1101 | Pasted a blog comparison | Opened `solutions/` first |
| Production awareness | Refuses EKS/ROSA/NAT in a 90-minute lab; Module 10 remains a valid home; no second control plane as rollback | Mentions cost without a refusal | Applied or recommended EKS as the lab path |
| Trade-off analysis | Task def vs Deployment; ALB health vs kubelet probes; who patches nodes; IAM models | One honest trade-off | “Kubernetes is always better” |
| Security / reliability | Task role ≠ execution role vs IRSA vs SA; secrets not in git in every column | Mentions IAM | Combined admin role as the ECS design |
| Communication | Table a Staff engineer could run at 02:00 | Readable table, thin paragraphs | Fragment notes |
| Efficiency | 60–90 minutes, complete PF-aws-platform.md | Complete but unfocused | Incomplete worksheet |

A recommendation to apply EKS or ROSA for this lab caps Production awareness at 1 regardless of table quality. “EKS is more production” as the EKS win caps Technical accuracy at 3 or below.
