# Infrastructure – Banking Regulatory Capstone

**Project key:** `cnde-cap-banking`  
**Tag:** `Project=capstone-option-1`

---

## Strategy: Reuse Course Lab Stack

This option does **not** ship a separate Terraform root. Capstone demos reuse the shared course lab environment already managed by:

```bash
# From repository root
./scripts/lab-cycle.sh start
```

That script provisions (or refreshes) the student data-lake bucket, IAM roles, and related lab resources used across Modules 3–10.

Optional helper from shared capstone tooling:

```bash
bash ../_shared/deploy-aws.sh
# equivalent to: repo-root ./scripts/lab-cycle.sh start
```

---

## Upload Capstone Outputs

After a successful local run:

```bash
export BUCKET=<lab-datalake-bucket-name>

cd capstone/projects/option-01-banking-regulatory
python3 ../_shared/run_pipeline.py --project-root . --upload --bucket "$BUCKET"
```

Objects appear under:

```text
s3://$BUCKET/capstone/cnde-cap-banking/
  raw/ ... cleaned/ ... curated/ ... quarantine/ ... metadata/
```

---

## Required Tags

Apply (or confirm) these tags on lab resources you touch for this option:

| Key | Value |
|-----|-------|
| `Project` | `capstone-option-1` |
| `Course` | `cloud-native-data-engineering` |
| `Environment` | `dev` |
| `Owner` | `cnde-cap-banking` |

Example CLI tag on the bucket (adjust name):

```bash
aws s3api put-bucket-tagging --bucket "$BUCKET" --tagging \
  'TagSet=[{Key=Project,Value=capstone-option-1},{Key=Owner,Value=cnde-cap-banking}]'
```

---

## Glue Job (Optional)

Upload `src/etl/glue_job.py` to the lab scripts bucket / Glue job definition used in class. Pass:

| Argument | Example |
|----------|---------|
| `--BUCKET` | `$BUCKET` |
| `--PROCESSING_DATE` | `2024-01-15` |
| `--PROJECT` | `cnde-cap-banking` |

---

## Teardown

When finished with demos:

```bash
./scripts/lab-cycle.sh stop
# or follow course teardown / terraform destroy for the lab stack
```

Leaving idle lab resources running is the primary student cost risk—see `docs/COST-ANALYSIS.md`.
