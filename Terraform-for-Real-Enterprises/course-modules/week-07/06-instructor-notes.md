# Week 7 — Instructor Notes

## Pre-class checklist

- [ ] Confirm Checkov installed or provide `pip install checkov` instructions
- [ ] Review Week 2 IAM policy students will modify
- [ ] Share example security report (redacted) from prior cohort if available
- [ ] Verify `.checkov.yml` in `labs/week-07/`

## Timing adjustments

| If running short | Cut |
|------------------|-----|
| 30 min | OPA/Conftest section to reading |
| 20 min | Access Analyzer to optional |

| If running long | Add |
|-----------------|-----|
| 30 min | Live CI job failing Checkov; fix and re-run |
| 20 min | Tag policy SCP whiteboard (no AWS apply required) |

## Live demo script — Checkov (15 min)

1. Introduce intentional misconfiguration in branch (e.g. open SG in module comment block—use fake resource)
2. Run Checkov; show CKV ID
3. Fix; document skip with ticket for one acceptable lab finding

## Live demo script — IAM trim (10 min)

1. Show `ec2:*` in policy
2. Replace with describe + run instances actions needed for lab
3. Attempt apply—add missing action from error message (teaches iterative least privilege)

## Common student mistakes

| Mistake | Teaching moment |
|---------|-----------------|
| Skipping all Checkov failures via skip list | Exception process |
| Tags only in `tags = {}` block, not default_tags | Incomplete coverage |
| Storing Checkov JSON with secrets | Redact paths |
| OIDC trust `*` repo | Condition on repo ref |

## Discussion prompts

1. “Can Terraform alone achieve SOC2?”
2. “Who owns policy exceptions?”
3. “Plan-time vs apply-time enforcement?”

## Accessibility

- Provide pre-scanned Checkov output for students who cannot run local scans
- Screen reader: CLI output exported to text file

## Link to capstone

Distribute capstone options; require track selection by end of Week 7 if Week 8 starts immediately.
