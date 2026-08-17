# Lab 8 — Capstone integration

**Week 8 · Estimated time: 8+ hours**

> **Terraform:** Use full lab stack as capstone foundation; extend in `infra/environments/lab/` or fork modules. **Destroy when finished:** `./scripts/stop_stack.sh --yes`.

## Objectives

Integrate labs 1–7 into one **demo path** per your capstone track. See [../capstone.md](../capstone.md).

## Minimum integration path (all tracks)

1. File arrives (SFTP or S3 upload).  
2. Validation / workflow executes.  
3. Status visible via API or runbook query.  
4. Outbound or completion notification (SNS/email/log).  

## Suggested demo script (10 minutes)

| Min | Action |
|-----|--------|
| 0–2 | Problem statement + architecture slide |
| 2–4 | Show self-serve catalog / API |
| 4–7 | Live transfer + Step Functions execution |
| 7–9 | Security + audit evidence (KMS, logs) |
| 9–10 | Roadmap: prod hardening, BayAreaLa8s consulting option |

## Repository layout

```
submissions/capstone/
  README.md
  architecture/
    diagram.png
    decision-log.md
  iac/                 # Terraform or CDK skeleton
  demo/
    DEMO_SCRIPT.md
    recording-link.txt
  security/
    threat-model-summary.md
```

## Rubric

See [../capstone.md](../capstone.md) — 35% of course grade.

## Cleanup

Run destroy script or manual teardown; confirm $0 Transfer servers left running.
