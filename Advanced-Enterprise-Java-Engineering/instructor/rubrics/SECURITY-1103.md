# Rubric — SECURITY-1103 IAM, secrets and KMS

**Type:** SECURITY (awsLab)  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

Score each dimension 0–100, then apply the weight. A live Secrets Manager apply must not be required to pass.

| Dimension | Weight | 100 | 60 | 20 |
|---|---|---|---|---|
| Technical accuracy | 25% | Two roles; execution has ECR + logs + one secret + one CMK; task def `valueFrom` ARNs with JSON keys; no plaintext | Split roles but `Resource: "*"` on the secret, or missing KMS | Combined role or `AdministratorAccess` remains |
| Diagnostic method | 20% | Listed starter defects (admin, combined ARN, `changeme`) before editing | Tightened “by feel” | Opened `solutions/` first |
| Production awareness | 15% | AEJE-D-050; Avery identifiers; Module 10 Secret vs task JSON; `us-west-2` ARNs | Mentions secrets vaguely | Recommends leaving `changeme` until prod |
| Trade-off analysis | 15% | Injected `secrets` vs app SDK; CMK vs AWS-managed key; one secret/three keys vs three secrets | One honest trade-off | Combined admin role as the lasting design |
| Security / reliability | 10% | No plaintext; no admin; task ≠ execution; KMS principal is the execution role | Split only, secret still in env | Password in JSON or admin on the task |
| Communication | 10% | PF-aws-platform IAM section complete | Files only | Empty worksheet |
| Efficiency | 5% | JSON + checklist; apply extra | Finished in session | Applied EKS/RDS/NAT as if required |

**Pass guideline:** weighted score ≥ 70, two roles, no `AdministratorAccess`, no secret literals in the task definition. `GetSecretValue` on the task role without a reason caps Technical accuracy at 60 or below. Optional apply neither raises nor lowers the score.
