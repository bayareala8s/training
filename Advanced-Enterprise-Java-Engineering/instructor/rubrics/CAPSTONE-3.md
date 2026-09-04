# Rubric — CAPSTONE-3 Cloud BayPay

**Type:** CAPSTONE (`awsLab`: true)  
**After:** Modules 11–12  
**Duration:** 4–8 hours  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

Score each dimension 0–100, then apply the weight. `terraform apply` absence must **not** fail the capstone. A packet that still health-checks `/`, silently writes a **99.99%** SLO, or applies NAT/EKS/RDS Multi-AZ is not a high score.

| Dimension | Weight | 100 | 60 | 20 |
|---|---|---|---|---|
| Technical accuracy | 25% | AEJE-D-072; `us-west-2`; health `/actuator/health/liveness` on **8080** matcher 200; `containerPort = 8080`; ECR immutable (not `:latest`); Fargate 256/512; SLO **99.9%** named; `terraform validate` green on a real tree or a cited composition plus the ALB contract | Most contracts present; path **or** port **or** SLO thin; modules hollow but root validates | Starter/skeleton unchanged; path `/`; `:latest` as the deploy tag; SLO only 99.99% with no upgrade sentence |
| Diagnostic method | 20% | Listed ACCOUNT.md + D-072 + OBSERVABILITY.md gaps before editing; synthesized BUILD-1101/1201/1202/1103/1105 rather than pasting blogs | Edited until it “looked like” a cloud deck | Opened `solutions/CAPSTONE-3/` first |
| Production awareness | 15% | ECS is apply default; EKS/OpenShift have honest **design** wins; tags `Course=AEJE Module=Capstone Lab=CAPSTONE-3 Environment=student Expiration`; idle ALB priced; destroy same day; no NAT/EKS/RDS apply; Avery port 8080 | Terraform works on paper; production names thin; destroy vague | Applied or required EKS/NAT/RDS Multi-AZ “for realism”; left an ALB overnight; bounce `dmgr-east` as stabilize |
| Trade-off analysis | 15% | Public+IGW vs NAT; ECS vs EKS vs OpenShift; module contract vs live `aws_ecs_service`+ALB; CPU scale vs SLO-adjacent scale; `valueFrom` vs app SDK; last-healthy tag vs `:latest` | One honest trade-off | “Kubernetes is always better”; NAT as the lasting student shape |
| Security / reliability | 10% | Execution ≠ task; no `AdministratorAccess`; `valueFrom` ARNs; named CMK; 404 ≠ SG miss; SLO burn paging; replica cap; heap ≠ Fargate limit | Roles split **or** secrets paper-only with a leftover `changeme` comment | Combined admin role; plaintext `BAYPAY_DB_PASSWORD`; `AKIA` in files; matcher includes 404 as design |
| Communication | 10% | PF-cloud.md a Staff engineer could run at 02:00; mermaid/service list; cost multiply shown | Incomplete excerpt; validate claimed without a command | Empty worksheet |
| Efficiency | 5% | 4–8 hours; validate-only (or apply + same-day destroy) | Finished in session, unfocused | Applied EKS/NAT/RDS as if required; re-solved every Module 11 lab from scratch without synthesizing |

**Pass guideline:** weighted score ≥ 70; health path is the Actuator liveness URL; `containerPort` is 8080; SLO is **99.9%** (99.99% only if named as Module 14); no secret values; no NAT/EKS/RDS Multi-AZ apply; `terraform validate` is the bar. Optional apply neither raises nor lowers Technical accuracy. Leaving path `/` caps Technical accuracy at 60 or below. A recommendation to apply EKS or ROSA for this capstone caps Production awareness at 20 or below regardless of table quality. “EKS is more production” as the only EKS win caps Technical accuracy at 60 or below. Opening `solutions/CAPSTONE-3/` before attempting PF-cloud.md caps Diagnostic method at 20 or below. An ALB left overnight caps Production awareness at 20 or below.
