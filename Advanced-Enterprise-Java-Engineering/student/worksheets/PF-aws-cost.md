# Portfolio worksheet — AWS cost (Module 11)

**Artifact:** [COST-1105](../../labs/COST-1105/README.md)  
**Course:** Advanced Enterprise Java Engineering  
**Case study:** BayPay Financial Services (fictional)  
**Diagram:** AEJE-D-052 (Cost optimization levers)  
**Also copy headline numbers to:** [PF-aws-platform.md](PF-aws-platform.md) section 7

Use the teaching rates from COST-1105 unless you cite a public pricing page (region `us-west-2`, date, URL). Show the multiply. Do not paste `solutions/COST-1105/`. Do not apply NAT, EKS, or RDS to “measure.”

**Student:**  
**Date:**  
**Did you apply anything this module?** (yes/no — if yes, say whether it is already destroyed)

---

## 1. Rates you used

| SKU | Rate | Source (course table or URL + date) |
|---|---|---|
| ALB-hour | | |
| Fargate vCPU-hour | | |
| Fargate GB-hour | | |
| t3.small-hour | | |
| NAT Gateway-hour | | |
| EKS control-plane-hour | | |
| ECR GB-month | | |

Fargate 256/512 hourly (show vCPU + GB):

---

## 2. Windows

| Resource | 1.5 h | 24 h | 7 d |
|---|---|---|---|
| ALB (LCU ≈ 0) | | | |
| Fargate one task 256/512 | | | |
| t3.small always-on | | | |
| NAT (refused) | | | |
| EKS control plane (refused) | | | |
| ECR 2 GB | — | — | |

Same-day session range you would brief before `apply` (USD):

Overnight idle ALB (one sentence):

---

## 3. Fargate versus always-on EC2

Which wins for a lab you destroy the same day, and why?

When would Fargate cost more than a packed instance, and why is that the wrong comparison here?

---

## 4. Refusals

**NAT for a 90-minute lab** (dollars + isolation trade-off):

**EKS control plane** (dollars/day):

**RDS / always-on EC2 / Container Insights** (one line each):

---

## 5. What still bills

After `desired_count = 0`:

After the ECS service is deleted but the ALB remains:

After the ALB is gone but ECR images remain:

---

## 6. Destroy checklist

- [ ] ALB, listener, target group
- [ ] ECS service, cluster, task definition
- [ ] ECR repository **and images**
- [ ] CloudWatch log group
- [ ] Confirmed no NAT, no EKS, no RDS
- [ ] `Expiration` tag was a reminder — you still ran destroy

Notes (account alias, stack dir, date destroyed):

---

## 7. Interview snippet (4–6 sentences)

Tell Finance why the idle ALB was the weekend line item, why NAT was the wrong “fix,” and what you will destroy before you leave.
