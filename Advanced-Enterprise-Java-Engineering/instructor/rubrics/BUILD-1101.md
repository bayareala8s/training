# Rubric — BUILD-1101 Deploy BayPay on ECS/Fargate

**Type:** BUILD (awsLab)  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

Score each dimension 0–100, then apply the weight. `terraform apply` absence must not fail the lab. A target group that still health-checks `/` is not a high Technical score.

| Dimension | Weight | 100 | 60 | 20 |
|---|---|---|---|---|
| Technical accuracy | 25% | `health_check.path` = `/actuator/health/liveness` on 8080 matcher 200; `containerPort = 8080`; Fargate 256/512; `us-west-2`; no NAT/EKS/RDS | Path or port fixed, not both; or cpu/memory oversized | Starter unchanged (`/` default, no `containerPort`) |
| Diagnostic method | 20% | Listed starter gaps (path `/`, missing port) against ACCOUNT.md before editing | Edited until it “looked like” a blog module | Opened `solutions/` first |
| Production awareness | 15% | Names ECR `baypay/payment-service`, Avery port 8080, tags + Expiration, H2/`local` so RDS stays out | Terraform works on paper; no production names | Treats the file as a local demo only, or adds RDS/EKS |
| Trade-off analysis | 15% | Public subnet + IGW vs NAT; ALB vs NLB; Fargate vs always-on EC2 (deferred to COST-1105) | States a preference with little why | Adds NAT “for realism” |
| Security / reliability | 10% | Separate execution vs task role; no secret `environment`; health path not `/` | Roles combined **or** a convenience password | `AdministratorAccess` on the task, or plaintext `BAYPAY_DB_PASSWORD` |
| Communication | 10% | Checklist complete; PF-aws-platform deploy section readable | Incomplete excerpt | Empty worksheet |
| Efficiency | 5% | Checklist + `validate` only; apply extra | Finished in session | Applied EKS/NAT/RDS as if required |

**Pass guideline:** weighted score ≥ 70, health path is the Actuator liveness URL, `containerPort` is 8080, no secret values, no NAT/EKS/RDS. Optional apply neither raises nor lowers the score. Leaving path `/` caps Technical accuracy at 60 or below.
