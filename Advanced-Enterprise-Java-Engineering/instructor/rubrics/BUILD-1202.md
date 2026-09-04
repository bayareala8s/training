# Rubric — BUILD-1202 Reusable Terraform modules

**Type:** BUILD  
**awsLab:** yes  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

Score each dimension 0–100, then apply the weight. A hollow `modules/` directory with ECR inlined in the root is not a high Technical score. `apply` absence must not fail the lab.

| Dimension | Weight | 100 | 60 | 20 |
|---|---|---|---|---|
| Technical accuracy | 25% | `modules/ecr` + `modules/ecs_service`; port default 8080; health path default `/actuator/health/liveness`; `region` default `us-west-2` on root and modules; `required_providers.aws`; `terraform validate` | One module complete; port or health missing | Starter unchanged |
| Diagnostic method | 20% | Listed missing port/health/repository before editing | Copied 1201 into both folders | Opened `solutions/` first |
| Production awareness | 15% | Image not `:latest`; ACCOUNT.md tags; AEJE-D-055 cited; no ALB | Modules exist; `:latest` still passed | Applied ALB/Fargate from this lab |
| Trade-off analysis | 15% | Module vs root copy; log-group stand-in vs live `aws_ecs_service`; why port is a variable | Preference with little why | No trade-off |
| Security / reliability | 10% | No keys; immutable image input; least-privilege named (ECR + logs) | No keys; `:latest` allowed | Access key in module source |
| Communication | 10% | PF-iac modules section; port and health path written out | Incomplete excerpt | Empty worksheet |
| Efficiency | 5% | Validate only | Finished in session | NAT/EKS/ALB applied |

**Pass guideline:** weighted score ≥ 70, both modules present, port 8080 and liveness path declared, validate green. Health variable name may be `health_path` or `health_check_path`.
