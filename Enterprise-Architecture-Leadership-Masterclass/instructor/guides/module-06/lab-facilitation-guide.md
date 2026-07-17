# Lab Facilitation Guide — Module 06

**Lab:** Build NorthStar’s Integration Reference Architecture  
**Student path:** `labs/lab-06-integration-platform/`  
**Terraform:** `infrastructure/terraform/environments/lab06/`  
**Cleanup:** `infrastructure/terraform/scripts/cleanup-lab06.sh`

---

## Setup (before class)

- Validate `terraform apply` in instructor account; capture sample outputs
- Confirm instructor SNS email subscription works end-to-end
- Prep EventBridge put-events JSON snippet (source + detail-type)
- Keep reference solution private (`instructor/reference-solutions/module-06/`)
- Announce budget alert + required tags

## Launch script (2 min)

> You are Lead EA at NorthStar (fictional). Deploy the reference architecture that proves sync, event, file, and workflow patterns—then document why each pattern fits. Transfer Family is conceptual only; use S3 landing. Forty minutes live. Confirm SNS. Destroy before you leave. Artifacts beat perfection.

## Progress checkpoints

| Time | Check |
| ---- | ----- |
| +10 min | Apply started or outputs available; tags present |
| +15 min | Account API POST/GET evidence |
| +25 min | Payment event → SQS path working (or debug EventBridge JSON) |
| +30 min | Partner file S3 put + Lambda evidence |
| +35 min | Force matrix + ADR writing even if SFN pending |
| +40 min | Cleanup plan spoken; evidence screenshots saved |

## Stuck-student prompts

- “Which failure mode are you designing for—timeout, duplicate, poison, or late file?”
- “Who owns the meaning of that event name?”
- “What would Transfer Family buy you that S3 landing does not—in dollars and ops?”

## Facilitation risks

- SNS confirmation delays (start email confirm early)
- EventBridge source/detail-type typos
- Students over-scoping Transfer Family or NAT/EKS
- Silent notify failures without confirmed subscription

## Review selection

Prefer one strong pattern matrix with ownership clarity and one ADR with real cost trade-offs—not the flashiest Mermaid.
