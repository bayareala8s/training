# INCIDENT-1104 — Unhealthy ALB target

**Type:** INCIDENT (awsLab)  
**Module:** 11 — AWS Container Platforms  
**Duration:** 45–75 minutes  
**Cost:** $0 for the pack; **billable if BUILD-1101 leftovers still exist**  
**Lessons:** L-11.4, L-11.6 (symptoms only — lessons do not name the cause)  
**Diagram:** AEJE-D-051 (Unhealthy ALB target)  
**Pack:** [incidents/aws/INC-AWS-1104](../../incidents/aws/INC-AWS-1104/README.md)

This student guide does **not** contain a root-cause answer. Work the evidence in gate order. You do not need to `terraform apply`.

---

## Scenario

14:10 Pacific on a synthetic `us-west-2` afternoon in November 2026. Harbor Market reports HTTP 502/503 on `pay-alb-student.baypay.example`. The pager names `payment-service` and an unhealthy ALB target group. Teaching paste shows ECS tasks **RUNNING**. You are the engineer on call. The incident pack is synthetic BayPay data.

---

## Business context

Avery Chen’s client (`11111111-1111-1111-1111-111111111111`, active USD account `22222222-2222-2222-2222-222222222221`) retries when a create payment does not return. A 502/503 from the ALB is not a domain decline. Finance does not care that `ecs describe-tasks` shows `RUNNING`. They care that the target group has nobody healthy to send traffic to.

Do not bounce RDS (this estate has no student RDS). Do not bounce `dmgr-east`. Probe contracts come from BUILD-305, BUILD-1101, and [datasets/baypay-aws/ACCOUNT.md](../../datasets/baypay-aws/ACCOUNT.md). A live account is **not** required.

---

## Learning objectives

- Follow gated evidence: target health first, then the task definition, then the listener/curl paste.
- Treat **RUNNING** as a container-process fact, not as “the ALB can take traffic.”
- Separate a health-check **HTTP 404** (packet arrived) from a security-group miss (timeout / connection refused).
- Write stabilization that restores healthy targets without pretending a bounce or a wider SG fixes a 404.
- Produce a comms update that does not invent a database outage or an SG outage before target health supports it.

---

## Architecture

Course diagram **AEJE-D-051** is this path. Until the PNG is on disk, use the text plus ACCOUNT.md.

**Region:** `us-west-2`.

**Service list (this incident):** ALB, listener, target group, ECS service, Fargate task, CloudWatch (literacy). **Not in the pack as live resources:** NAT, EKS, RDS.

```text
Merchants / Avery Chen
  → ALB pay-alb-student.baypay.example  (or AWS DNS)
       → listener :80 forward
            → target group  port 8080  (health check path is in evidence)
                 → Fargate task  lastStatus RUNNING
                      Spring Actuator groups    (BUILD-305 / ACCOUNT.md)
```

One process, two questions: is the task running, and does the **target group** consider it healthy? You do not need a live account. The contracts are RUNNING, unhealthy targets, and the HTTP status the health check received.

**Least privilege:** read-only `elasticloadbalancing:Describe*`, `ecs:Describe*`. Do not attach admin to diagnose. Do not open the VPC to `0.0.0.0/0` on 8080 as a “fix.”

**Failure scenario:** merchants 502/503 while tasks stay RUNNING and the target group is unhealthy. Stabilization and remediation are different sentences (change the path now; bake it into Terraform so `/` cannot return).

---

## Prerequisites

- BUILD-1101 attempted (you know the ALB + Fargate shape, even on paper).
- BUILD-305 (liveness / readiness / aggregate health) completed, or read in the same sitting.
- Locked names from [datasets/baypay-aws/ACCOUNT.md](../../datasets/baypay-aws/ACCOUNT.md).
- Incident worksheet: [student-worksheet.md](../../incidents/aws/INC-AWS-1104/student-worksheet.md).
- Optional PAKS: `docs/16-cloud-architecture/aws-fundamentals.md`. Lessons stand alone without it.

---

## Environment setup

No runtime required. Open the pack:

```text
incidents/aws/INC-AWS-1104/
  README.md
  timeline.json
  student-worksheet.md
  evidence/          # gated — see timeline.json "gates"
```

This pack is a **gated subset**. Gate 1 is target health. Gate 2 is the task-definition excerpt. Gate 3 is the ALB listener / merchant curl paste. The pack README documents what shipped and what was omitted.

Do not open `solutions/INCIDENT-1104/` until you have filled the worksheet through remediation.

Do not run `aws` against a paid or shared account to “reproduce.” The files are the account. If you still have BUILD-1101 leftovers, they are a **cost** problem (COST-1105), not extra evidence.

---

## Challenge/tasks

1. Read the pack README and `timeline.json`. Note who shipped the task definition or target group, and when 502/503s began.
2. **Gate 1:** open `evidence/target-health.txt` only. Record target state, health-check port, health-check path, and the status code or reason. Write a first hypothesis and the next investigation.
3. **Gate 2:** after that hypothesis, open `evidence/task-def.json`. Update the hypothesis. Quote `lastStatus`, `containerPort`, and anything that confirms the process is up.
4. **Gate 3:** open `evidence/alb-listener.txt` only if it answers a question you already wrote about the edge versus the task.
5. Write stabilization, remediation, and a 5-line comms update. Name people only as they appear in the timeline (Priya Nair, Riley Okonkwo, Sam Okada).
6. Optional: one sentence mapping BUILD-305 / ACCOUNT.md (`/actuator/health/liveness`) to the target-group path — literacy only.

---

## Validation

A complete worksheet has all six fields: hypothesis (updated per gate), evidence, next investigation, stabilization, remediation, comms. A lucky “SG” (security group) with no path-versus-Actuator comparison scores low on Diagnostic method (see rubric). Skipping to the listener curl before a written question also scores low. Opening the solution first fails Diagnostic method.

**Expected final state:** a written diagnosis path an instructor can score. You may be wrong on the first hypothesis; you may not skip gates. The student guide will not tell you which path the target group uses.

---

## Troubleshooting

- You jumped to later files: stop, write what you *would* have asked, then continue.
- Tasks are RUNNING and merchants see 502/503: RUNNING is not healthy. Table it.
- You want application `logs.txt`: they are omitted. Write what a **404** on the health path would look like versus a connect timeout (SG / wrong port).
- You are about to widen the task security group to `0.0.0.0/0`: re-read whether the health check already received an HTTP code.
- You are about to bounce RDS or `dmgr-east`: re-read ACCOUNT.md.
- You copied INCIDENT-1003’s kube readiness story: same *class* of bug, different object (target group, not kubelet). Quote ALB evidence.
- You want to `terraform apply` a live fix: write the change on paper. This lab does not require an account.

---

## Expected outcome

A written diagnosis path an instructor can score. Stabilization restores a 200 on the health check. Remediation bakes that path into the Terraform module so `/` cannot come back. The student guide will not name the path.

---

## Interview questions

1. Why is “the tasks are running” a weak first sentence when the target group is unhealthy?
2. What does an HTTP **404** on the health check prove that a 502 from the ALB does not?
3. Why is “open the security group” a weak first fix if the health check already received an HTTP status?
4. When do you change the target-group path versus add a controller that serves `/`?
5. How does an unhealthy target explain a 502/503 without blaming PostgreSQL?

---

## Architecture/trade-off questions

1. Who owns the contract that the ALB path matches BUILD-305 groups — app repo or Terraform module?
2. Should a CI check `terraform plan` (or a policy) fail when `health_check.path` is `/`?
3. Why is a single `/` health check a reliability smell for a Spring Boot API with no static index?
4. What do you lose if the matcher accepts `404` “so the ALB goes green”?

---

## Cleanup

None for the pack. Do not delete the evidence files. No live cluster to delete.

**If BUILD-1101 leftovers still exist in `us-west-2`:** destroy the ALB, ECS service/cluster, and ECR images **today**. An idle ALB still bills. This incident pack did not ask you to apply.

---

## Cost estimate

**$0.** Synthetic files only. No required AWS API. No paid EKS.

**Warning:** if you left BUILD-1101 applied, you are already paying ALB (~$0.0225/hour) and Fargate. That bill is not part of this lab’s grade. Destroy those leftovers. Teaching estimates in USD.

---

## Hidden/revealable solution

The student guide does not include the answer. Submit the worksheet first. Instructors use `solutions/INCIDENT-1104/` and `instructor/rubrics/INCIDENT-1104.md`. Opening the solution before you write is a failed diagnostic method score.

---

## What you learned

RUNNING is not healthy. Target-group HTTP status, task status, and the merchant 502/503 have to be read together. A 404 means the packet arrived — so “SG” is a lucky guess unless you show a timeout. Stabilization (change the path to a 200) is a different sentence from remediation (bake the path into Terraform; never `/`).

---

## Portfolio deliverable

Attach the completed INC-AWS-1104 worksheet to your notes. The Module 11 portfolio artifact is [student/worksheets/PF-aws-platform.md](../../student/worksheets/PF-aws-platform.md): write a short incident inset (symptom, what you ruled out, stabilize vs remediate) if this is the AWS incident you will keep.
