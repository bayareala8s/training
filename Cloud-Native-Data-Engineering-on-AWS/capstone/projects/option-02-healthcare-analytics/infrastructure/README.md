# Infrastructure – Healthcare Analytics Capstone

**Project key:** `cnde-cap-healthcare`  
**Tag:** `Project=capstone-option-2`

---

## Strategy: Reuse Course Lab Stack

Do not deploy a separate Terraform root for this option. Reuse the shared course lab environment:

```bash
# From repository root
./scripts/lab-cycle.sh start
```

Shared helper:

```bash
bash ../_shared/deploy-aws.sh
```

---

## Upload Capstone Outputs

```bash
export BUCKET=<lab-datalake-bucket-name>

cd capstone/projects/option-02-healthcare-analytics
python3 ../_shared/run_pipeline.py --project-root . --upload --bucket "$BUCKET"
```

Prefix:

```text
s3://$BUCKET/capstone/cnde-cap-healthcare/
```

Ensure analyst roles cannot read `raw/` or `cleaned/` in shared buckets when demonstrating HIPAA-aware access patterns.

---

## Required Tags

| Key | Value |
|-----|-------|
| `Project` | `capstone-option-2` |
| `Course` | `cloud-native-data-engineering` |
| `Environment` | `dev` |
| `Owner` | `cnde-cap-healthcare` |
| `DataClassification` | `Restricted-PHI-Synthetic` |

```bash
aws s3api put-bucket-tagging --bucket "$BUCKET" --tagging \
  'TagSet=[{Key=Project,Value=capstone-option-2},{Key=Owner,Value=cnde-cap-healthcare}]'
```

---

## Glue Job (Optional)

Point a lab Glue job at `src/etl/glue_job.py` with:

| Argument | Example |
|----------|---------|
| `--BUCKET` | `$BUCKET` |
| `--PROCESSING_DATE` | `2024-01-15` |
| `--PROJECT` | `cnde-cap-healthcare` |

---

## Teardown

```bash
./scripts/lab-cycle.sh stop
```

See `docs/COST-ANALYSIS.md` for budget guidance.
