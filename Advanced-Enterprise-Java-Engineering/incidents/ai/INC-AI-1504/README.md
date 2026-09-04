# INC-AI-1504 — ALB 502/503 while payment tasks stay RUNNING (AI evaluation pack)

**Lab:** AI-1504  
**Severity:** SEV-2  
**Service:** payment-service (ECS/Fargate, `us-west-2`)  
**When:** 2026-09-03 14:10 Pacific (21:10 UTC)  
**Data:** Synthetic BayPay. Not a real outage.

This is a **small single pack**. All shipped evidence is available after you read this page and `timeline.json`. There is no hidden database file.

The planted BayOps JSON you evaluate lives at [infrastructure/bayops-ai/fixtures/ai-1504-hallucination.json](../../../infrastructure/bayops-ai/fixtures/ai-1504-hallucination.json). That file is the **artifact to grade**, not a prior lab’s RCA.

Record work on [student-worksheet.md](student-worksheet.md) and [student/worksheets/PF-ai.md](../../../student/worksheets/PF-ai.md).

This pack does not include a root-cause statement. Filenames and titles describe the **ALB / target-health symptom class** only. Do not import a prior module’s RCA as if it were proven here.

## Evidence shipped versus omitted

| Kind | In this pack? |
|---|---|
| Timeline | Yes — `timeline.json` |
| ECS task describe | Yes — `evidence/ecs-tasks.txt` |
| ALB merchant curl + target health | Yes — `evidence/alb-and-targets.txt` |
| Pack inventory | Yes — `evidence/pack-inventory.txt` |
| Application logs.txt | **Omitted** |
| Thread dumps | **Omitted** |
| Deployment history | **Omitted** |
| Database metrics | **Omitted** — there is no writer CPU, no RDS event, no Multi-AZ file |
| `evidence/db-failover.json` | **Not shipped.** If a model cites it, the citation is invented. |
| `dmgr-east` / PaymentCluster dumps | **Omitted** — leftover ND is not on the merchant path |

If you believe you need an omitted kind, write *why* and what you expect it to show. Do not invent numbers. Do not create `db-failover.json` to “match the model.”
