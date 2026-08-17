# Infrastructure – Option 3 E-Commerce Analytics Lakehouse

**Project key:** `cnde-cap-ecommerce`  
**Tag:** `Project=capstone-option-3`

This capstone reuses the course lab stack instead of maintaining a separate Terraform root. The shared helper wraps `scripts/lab-cycle.sh`.

## Prerequisites

- AWS CLI configured (`aws sts get-caller-identity`)
- Course repo root with Terraform labs deployable
- Python 3.10+ for the local pipeline

## Deploy (optional AWS path)

From the course repository root:

```bash
./scripts/lab-cycle.sh start
source ./scripts/lab-env.sh   # loads $BUCKET and related vars
```

Or via the shared capstone helper:

```bash
bash ../../_shared/deploy-aws.sh
```

Tag resources (or verify tags) for this option:

```text
Project=capstone-option-3
Course=cloud-native-data-engineering
Environment=dev
Owner=capstone-student
```

## Upload local pipeline output

After a successful local run:

```bash
cd ..
bash scripts/run_local.sh --upload --bucket "$BUCKET"
# writes under s3://$BUCKET/capstone/cnde-cap-ecommerce/
```

## Glue job (optional)

Upload `src/etl/glue_job.py` to the lab Glue scripts prefix and start a job run with:

| Argument | Example |
|----------|---------|
| `--raw_bucket` | `$BUCKET` |
| `--cleaned_bucket` | `$BUCKET` |
| `--curated_bucket` | `$BUCKET` |
| `--processing_date` | `2024-01-15` |

## Teardown

```bash
./scripts/lab-cycle.sh stop --yes
```

Stopping the lab stack returns ongoing AWS cost to near zero (KMS keys may remain in pending-deletion for 7 days if Lab 7 was exercised).
