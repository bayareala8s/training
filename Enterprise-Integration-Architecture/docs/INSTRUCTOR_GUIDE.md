# Instructor guide — Enterprise Integration Architecture

## Before the cohort

1. Read `COURSE.md`, `GETTING_STARTED.md`, and `docs/STUDENT_HANDBOOK.md`.
2. Serve the player from the **repo root**: `./scripts/start_course.sh` → `/course-ui/`.
3. Run `python3 scripts/check_course.py` (catalog, labs, capstone Terraform).
4. Confirm sandbox accounts, region (`us-west-2` default), and a destroy policy.
5. `./scripts/seed_paper_labs.sh` copies samples into `submissions/` for a **validator smoke test**. Those copies **FAIL** integrity checks unless `EIA_ALLOW_SAMPLES=1`. Wipe `submissions/` before sharing a student workspace.

## Do not hand students the answer

| Artifact | Audience |
|----------|----------|
| `labs/lab-01-classification/sample-completed-worksheet.md` | Instructor smoke test only |
| `labs/lab-08-esb-modernization/reference/adr.md` | Instructor / after students submit |
| `./scripts/seed_paper_labs.sh` | Copies samples into `submissions/` for **your** validator check — wipe before sharing a workspace |

Grade **rationale and NFRs** harder than Terraform formatting.

## Lab operations

```bash
./scripts/lab_up.sh lab-02-api
python3 scripts/validate_lab.py lab-02-api
./scripts/lab_down.sh lab-02-api
```

Capstones: `banking`, `ecommerce`, `healthcare`, `manufacturing`.

- **Lab 12:** first apply is insecure. Students must see **FAIL**, then `insecure=false`, then **PASS**.
- **Lab 15:** Bedrock stays off (`enable_bedrock=false`) unless the account is enabled and you accept token cost. The mock planner `scripts/ops_agent.py` is the default.
- **Validators** hit live AWS (except Labs 1 and 8). A green `PASS` without apply is a bug — do not restore the old stub validators.

## Grading emphasis

| Signal | Band |
|--------|------|
| Style from NFRs; mixed patterns; residue named; agent HITL; cost | Distinction |
| Framework used; AWS named last; DLQ/idempotency present | Pass |
| Service-first; LLM→database; 10 GB through API Gateway; copied sample worksheet | Fail |

Oral defense (20 minutes) on the final assessment is recommended even when the player certificate has unlocked (the player is self-attestation).

## Generators

`tools/` regenerates lesson drafts. **Do not run generators during a live cohort** — they can overwrite student-facing markdown. Labs, Terraform, and `scripts/validate_lab.py` are hand-maintained.

## Certificate

Player completion is `localStorage` (self-paced). For LMS cohorts, mirror the rules in `COURSE.md` §8 in the BayLearn Portal / `lms/` manifests.

## Cleanup

```bash
./scripts/destroy_all.sh --yes
```
