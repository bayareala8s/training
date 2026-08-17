# Hands-on labs

Complete labs in order. Use a **non-production** AWS account.

## Terraform (recommended)

All labs share one stack. **Provision** and **destroy** to control cost:

```bash
./scripts/start_stack.sh --yes    # begin lab session
./scripts/stop_stack.sh --yes     # end session — stops AWS charges
```

Full guide: **[TERRAFORM-LABS.md](TERRAFORM-LABS.md)** · Infrastructure: **[../../infra/README.md](../../infra/README.md)**

Manual/console steps in each lab are optional where marked *Terraform provides*.

| Lab | Week | Est. hours | Guide |
|-----|------|------------|-------|
| 1 | 1 | 3 | [lab-01-transfer-family-sftp.md](lab-01-transfer-family-sftp.md) |
| 2 | 2 | 3 | [lab-02-security-hardening.md](lab-02-security-hardening.md) |
| 3 | 3 | 4 | [lab-03-s3-event-processor.md](lab-03-s3-event-processor.md) |
| 4 | 4 | 4 | [lab-04-step-functions-workflow.md](lab-04-step-functions-workflow.md) |
| 5 | 5 | 4 | [lab-05-sftp-connector.md](lab-05-sftp-connector.md) |
| 6 | 6 | 5 | [lab-06-self-serve-api.md](lab-06-self-serve-api.md) |
| 7 | 7 | 3 | [lab-07-observability.md](lab-07-observability.md) |
| 8 | 8 | 8+ | [lab-08-capstone-integration.md](lab-08-capstone-integration.md) |
| **9** | **5+** | **[lab-09-ecs-fargate-large-files.md](lab-09-ecs-fargate-large-files.md)** *(stretch)* |

**Lab 9** requires Docker for image build. Demo: `./scripts/demo_ecs_large_file.sh`

## Submission

Submit each week via LMS (or instructor-defined repo):

```
submissions/week-NN/
  README.md          # what you built, how to reproduce
  screenshots/       # proof of completion
  artifacts/         # diagrams, ASL, OpenAPI, etc.
```

## Grading

See [../assessment.md](../assessment.md) for rubrics.
