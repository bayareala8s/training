# COST-1105 — Instructor solution

**Do not share this file with students before they submit arithmetic.**

Teaching rates are the shared table from the student lab (USD, `us-west-2`). A student who used a live public pricing page and **showed the source** may differ by a few cents — accept if the method is honest. A table with no multiply is not a high Technical score.

## Check figures

Fargate 0.25 vCPU / 0.5 GB:

`0.25 × 0.04048 + 0.5 × 0.004445 = 0.01012 + 0.0022225 = 0.0123425 ≈ $0.01234/hour`

| Resource | 1.5 h | 24 h | 7 d |
|---|---|---|---|
| ALB @ $0.0225/h (LCU ≈ 0) | $0.0338 | $0.54 | $3.78 |
| Fargate 256/512 @ $0.01234/h | $0.0185 | $0.296 | $2.07 |
| t3.small @ $0.0208/h | $0.0312 | $0.499 | $3.49 |
| NAT @ $0.045/h (no data) | $0.0675 | $1.08 | $7.56 |
| EKS control plane @ $0.10/h | $0.15 | $2.40 | $16.80 |
| ECR 2 GB @ $0.10/GB-month | — | — | 2 × 0.10 × 7/30 ≈ $0.047 |

Same-day BUILD-1101 session (ALB + one task, 1–4 hours, then destroy): about **$0.15–$2.00** (ALB dominates; LCU can add a little if they hammer curl). Overnight idle ALB: **~$0.54**. Forgotten ALB + Fargate + ECR for a week: about **$5–$15** (ALB $3.78 + Fargate $2.07 + ECR pennies, plus any LCU or extra log ingest).

## Acceptable narrative

- **Idle ALB.** Bills by the hour with **zero** merchant traffic. Weekend leftover is the invoice Finance saw. Destroy same day.
- **Fargate vs t3.small.** For a 90-minute lab you destroy, Fargate is cheaper *and* goes to zero when `desired_count = 0` and the service/cluster are destroyed. Always-on EC2 still bills after the process exits. Fargate can cost more than a well-packed instance at 24/7 — that is the wrong comparison for this lab. Refuse always-on EC2 as the student default.
- **ECR.** Pennies per week at 2 GB, but images remain after the service is gone. `force_delete` plus an image purge is part of cleanup. Empty repos still store layers.
- **NAT.** ~$1.08/day before data — often more than the ALB. Public subnets + IGW + `assign_public_ip` is the locked student shape. Isolation trade-off: tasks have public IPs; do not pretend that is production-private. Do not add NAT for 90 minutes.
- **EKS / RDS.** Control plane ~$2.40/day before nodes. RDS is L-11.7 literacy; student apply uses `local` / H2. Neither is extra credit.

## Destroy checklist (must name all three)

1. ALB, HTTP listener, target group  
2. ECS service, cluster, task definition  
3. ECR repository **and images**  
4. CloudWatch log group (3-day retention still ingest-bills if left writing)  
5. Confirm no NAT, no EKS, no RDS  
6. `Expiration` tag is a reminder, not a delete API  

`desired_count = 0` stops Fargate hours; it does **not** stop the ALB.

## Diagram

AEJE-D-052: idle ALB, tiny Fargate, ECR storage on the bill; NAT / EKS / always-on EC2 rejected; same-day destroy of ALB, ECS, ECR.

## Scoring notes

Full marks require shown multiply (not a pasted total), ALB called out as the idle surprise, NAT and EKS refused with dollars, and a destroy list that names ALB, ECS, and ECR. Opening `solutions/` first fails Diagnostic method. Creating NAT or EKS “to measure” fails Production awareness and Efficiency.
