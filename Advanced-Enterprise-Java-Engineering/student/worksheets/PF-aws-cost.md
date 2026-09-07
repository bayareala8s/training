# Portfolio worksheet — AWS cost (Module 11)

**Artifact:** [COST-1105](../../labs/COST-1105/README.md)  
**Course:** Advanced Enterprise Java Engineering  
**Case study:** BayPay Financial Services (fictional)  
**Diagram:** AEJE-D-052 (Cost optimization levers)  
**Also copy headline numbers to:** [PF-aws-platform.md](PF-aws-platform.md) section 7

Use the teaching rates from COST-1105 unless you cite a public pricing page (region `us-west-2`, date, URL). Show the multiply. Do not paste `solutions/COST-1105/`. Do not apply NAT, EKS, or RDS to “measure.”

**Student:**  
**Date:** 2026-09-06  
**Did you apply anything this module?** **No** — BUILD-1101 `terraform validate` only. Nothing to destroy in `us-west-2`.

---

## 1. Rates you used

| SKU | Rate | Source (course table or URL + date) |
|---|---|---|
| ALB-hour | $0.0225 + LCU (lab LCU ≈ $0) | COST-1105 teaching table, `us-west-2` |
| Fargate vCPU-hour | $0.04048 | same |
| Fargate GB-hour | $0.004445 | same |
| t3.small-hour | $0.0208 | same |
| NAT Gateway-hour | $0.045 + data | same |
| EKS control-plane-hour | $0.10 | same |
| ECR GB-month | $0.10 | same |

Fargate 256/512 hourly (show vCPU + GB):

`0.25 × 0.04048 + 0.5 × 0.004445 = 0.01012 + 0.0022225 =` **$0.0123425/h ≈ $0.01234/h**

---

## 2. Windows

| Resource | 1.5 h | 24 h | 7 d |
|---|---|---|---|
| ALB (LCU ≈ 0) | `0.0225 × 1.5 =` **$0.03375** | `0.0225 × 24 =` **$0.54** | `0.54 × 7 =` **$3.78** |
| Fargate one task 256/512 | `0.01234 × 1.5 ≈` **$0.0185** | `0.01234 × 24 ≈` **$0.296** | `0.296 × 7 ≈` **$2.07** |
| t3.small always-on | `0.0208 × 1.5 =` **$0.0312** | `0.0208 × 24 =` **$0.499** | `0.0208 × 168 =` **$3.49** |
| NAT (refused) | `0.045 × 1.5 =` **$0.0675** | `0.045 × 24 =` **$1.08** + data | `1.08 × 7 =` **$7.56** + data |
| EKS control plane (refused) | `0.10 × 1.5 =` **$0.15** | `0.10 × 24 =` **$2.40** | `2.40 × 7 =` **$16.80** |
| ECR 2 GB | — | — | `2 × 0.10 × 7/30 =` **$0.0467** |

Same-day session range you would brief before `apply` (USD):

About **$0.15–$2.00** (lab estimate): 1–4 h ALB + Fargate (`1.5 h ≈ $0.05`; 4 h ALB $0.09 + Fargate $0.05 ≈ $0.14) plus a buffer if destroy slips an hour. Do not add NAT/EKS.

Overnight idle ALB (one sentence):

The ALB is **~$0.54/day even when Harbor Market sends zero traffic** — that line item, not the $0.012/h task, is the weekend surprise (`Thu night → Mon morning ≈ 3 × $0.54 ≈ $1.62` before LCU).

---

## 3. Fargate versus always-on EC2

Which wins for a lab you destroy the same day, and why?

**Fargate.** 1.5 h is **~$0.019** vs t3.small **~$0.031**, and `desired_count = 0` stops the task. You are not packing a week of density. Always-on `t3.small` is refused as the student default (ACCOUNT.md).

When would Fargate cost more than a packed instance, and why is that the wrong comparison here?

Fargate costs more when **many** tasks would fit on one EC2 (density / Reserved). That is a 24/7 fleet question. A 90-minute lab you destroy the same day is not a packing problem — and we still refuse always-on EC2 as the default.

---

## 4. Refusals

**NAT for a 90-minute lab** (dollars + isolation trade-off):

`0.045 × 1.5 = $0.0675` for the session; **$1.08/day + data** if forgotten — often **more than the idle ALB**. Public subnet + `assign_public_ip` + IGW is the locked student shape: you give up private-subnet isolation; you do **not** open 8080 to `0.0.0.0/0` to “avoid NAT.” SECURITY-1103 / BUILD-1101 already accepted that trade-off.

**EKS control plane** (dollars/day):

**$2.40/day** (`0.10 × 24`) before nodes — ~$73/month. Refused as a 90-minute “compare” (ARCHITECT-1102).

**RDS / always-on EC2 / Container Insights** (one line each):

RDS: literacy (L-11.7), not this apply — use `local` / H2. Always-on EC2: not the student default. Container Insights: another SKU; 3-day log retention already covers L-11.6 / INC-1104.

---

## 5. What still bills

After `desired_count = 0`:

**ALB** (~$0.0225/h), **ECR** storage, **log group**, IAM, VPC. The task stops; the front door does not.

After the ECS service is deleted but the ALB remains:

**Idle ALB + listener + TG** still ~$0.54/day. That is the weekend invoice.

After the ALB is gone but ECR images remain:

**ECR ~$0.10/GB-month** (2 GB ≈ $0.20/month; 7 d ≈ $0.047). Empty repo still bills. `force_delete` + delete images.

---

## 6. Destroy checklist

- [x] ALB, listener, target group — *nothing applied; would destroy these first*
- [x] ECS service, cluster, task definition
- [x] ECR repository **and images**
- [x] CloudWatch log group
- [x] Confirmed no NAT, no EKS, no RDS
- [x] `Expiration` tag was a reminder — you still ran destroy

Notes (account alias, stack dir, date destroyed):

Downloads workspace; `labs/BUILD-1101/work/` **validate only** (2026-09-06). No `us-west-2` stack. `Expiration=2026-09-06` is not a delete API.

---

## 7. Interview snippet (4–6 sentences)

Finance: the weekend line was the **idle ALB (~$0.54/day)**, not Avery’s $84 POST and not the **~$0.012/h** Fargate task. NAT “so Fargate could be private” is **~$1.08/day plus data** — more than the ALB — and is refused for a 90-minute lab; public + IGW + `assign_public_ip` is the student shape. EKS to compare is **~$2.40/day** before nodes. `desired_count = 0` does not stop the ALB; `Expiration` tags do not destroy. Before I leave: ALB + listener + TG, ECS service/cluster/task def, ECR **images**, log group — same day. No NAT, no EKS, no RDS.
