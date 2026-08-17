# Lab 4.1: Build a Data Quality Validation Framework

> 📊 **Diagrams:** [Mermaid](diagram.md) · [Draw.io (lab-4.1-quality-framework.drawio)](../../../../docs/diagrams/drawio/lab-4.1-quality-framework.drawio) · [PNG](../../../../docs/diagrams/png/lab-4.1-quality-framework.png) · [SVG](../../../../docs/diagrams/svg/lab-4.1-quality-framework.svg)

**Estimated time:** 120 minutes · **Module 4**

---

## Objectives

- Define validation rules in declarative JSON format
- Implement reusable validators (`not_null`, `range`, `enum`, `regex`)
- Run batch validation with pass/quarantine routing
- Generate a quality report with pass rates and violation breakdown
- Understand patterns applicable to Great Expectations and AWS Deequ

---

## Prerequisites

- Modules 1–3 complete (S3 data lake, sample orders data)
- Python 3.10+ with virtual environment active
- `boto3` installed (optional for S3 upload in Step 6)

---


## Platform Setup

From the **repository root**, start the shared lab environment (once per session):

```bash
./scripts/lab-cycle.sh start
source ./scripts/lab-env.sh
```

Stop when finished: `./scripts/lab-cycle.sh stop --yes` (avoids ongoing AWS charges).

---


## Architecture

```text
rules/orders_rules.json
        │
        ▼
┌───────────────────┐     sample-data/orders_sample.json
│  quality_runner   │ ←── (list of order records)
└─────────┬─────────┘
          │
          ├── validators.py (not_null, range, enum, regex)
          │
          ▼
    ┌─────┴─────┐
    ▼           ▼
 passed/    quarantine/
 (stdout)   (JSON file + report)
```

---

## Project Structure

```text
lab-4.1-quality-framework/
├── README.md
├── rules/
│   └── orders_rules.json
├── sample-data/
│   └── orders_sample.json
├── src/
│   ├── validators.py
│   └── quality_runner.py
└── output/          (created at runtime)
    ├── passed_records.json
    ├── quarantined_records.json
    └── quality_report.json
```

---

## Step 1: Review Validation Rules

Open `rules/orders_rules.json`:

```json
{
  "dataset": "retail/orders",
  "version": "1.0",
  "rules": [
    {
      "name": "order_id_not_null",
      "field": "order_id",
      "type": "not_null",
      "severity": "error",
      "message": "order_id is required"
    },
    {
      "name": "amount_in_range",
      "field": "order_amount",
      "type": "range",
      "params": { "min": 0.01, "max": 50000 },
      "severity": "error"
    },
    {
      "name": "status_valid",
      "field": "status",
      "type": "enum",
      "params": {
        "values": ["pending", "shipped", "delivered", "cancelled"]
      },
      "severity": "error"
    },
    {
      "name": "email_format",
      "field": "customer_email",
      "type": "regex",
      "params": {
        "pattern": "^[\\w.+-]+@[\\w.-]+\\.[a-zA-Z]{2,}$"
      },
      "severity": "warning"
    }
  ]
}
```

**Exercise:** Add a rule requiring `currency` to be in `["USD", "EUR", "GBP"]` with severity `error`.

---

## Step 2: Explore the Validator Library

Read `src/validators.py`. Each rule type implements a common interface:

| Function | Validates |
|----------|-----------|
| `validate_not_null(value, params)` | Value is not `None` or empty string |
| `validate_range(value, params)` | Numeric value within `min`/`max` |
| `validate_enum(value, params)` | Value in allowed `values` list |
| `validate_regex(value, params)` | Value matches `pattern` |

The `RuleEngine` class loads JSON rules and applies them to each record.

---

## Step 3: Run Local Validation

```bash
cd modules/module-04-data-quality/labs/lab-4.1-quality-framework

python src/quality_runner.py \
  --rules rules/orders_rules.json \
  --input sample-data/orders_sample.json \
  --output-dir output
```

Expected console output:

```text
Processed 10 records
  Passed:      7
  Quarantined: 3
  Pass rate:   70.00%
Report written to output/quality_report.json
```

Inspect results:

```bash
python -m json.tool output/quality_report.json
python -m json.tool output/quarantined_records.json
```

Each quarantined record includes `_violations` explaining why it failed.

---

## Step 4: Analyze Violations

Open `output/quarantined_records.json` and identify:

| Record | Failed Rule | Root Cause |
|--------|-------------|------------|
| `ORD-003` | `amount_in_range` | Negative amount (-15.99) |
| `ORD-007` | `status_valid` | Invalid status `returned` |
| `ORD-009` | `order_id_not_null` | Missing order_id |

**Discussion:** Record `ORD-005` has a malformed email but passes to cleaned—why? (Warning severity does not quarantine.)

---

## Step 5: Extend the Framework

Add a custom rule type or modify behavior:

**Option A — Composite unique check:** Extend `validators.py` with a batch-level `unique` validator on `order_id`.

**Option B — Strict mode:** Add CLI flag `--strict` that treats warnings as errors.

Test your change:

```bash
python src/quality_runner.py \
  --rules rules/orders_rules.json \
  --input sample-data/orders_sample.json \
  --output-dir output \
  --strict
```

With `--strict`, `ORD-005` should quarantine due to email format.

---

## Step 6: Upload Results to S3 (Optional)

If your Lab 1.1 bucket is deployed:

```bash
export BUCKET=$(cd ../../../../../infrastructure/environments/dev && terraform output -raw data_lake_bucket)
export DATE=$(date +%Y-%m-%d)
export YEAR=$(date +%Y)
export MONTH=$(date +%m)
export DAY=$(date +%d)

aws s3 cp output/quarantined_records.json \
  "s3://${BUCKET}/quarantine/retail/orders/year=${YEAR}/month=${MONTH}/day=${DAY}/quarantined_records.json"

aws s3 cp output/quality_report.json \
  "s3://${BUCKET}/metadata/quality-reports/retail/orders/${DATE}_report.json"
```

Verify:

```bash
aws s3 ls "s3://${BUCKET}/quarantine/retail/orders/" --recursive
aws s3 ls "s3://${BUCKET}/metadata/quality-reports/retail/orders/"
```

---

## Step 7: Document Your Work

Create `LAB-REPORT.md`:

```markdown
# Lab 4.1 Report

## Rules Configured
- List rules in orders_rules.json

## Validation Results
- Total / passed / quarantined counts
- Pass rate vs 99.9% SLO target

## Top Violations
| Rule | Count |
|------|-------|
| ... | ... |

## Extensions Implemented
- Describe Option A or B

## Screenshots
- quality_report.json summary
- S3 quarantine path (if uploaded)
```

---

## Deliverables

- [ ] `validators.py` and `quality_runner.py` run without errors
- [ ] At least one custom rule or `--strict` mode implemented
- [ ] `output/quality_report.json` generated
- [ ] `LAB-REPORT.md` with results table

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: validators` | Run from lab root; or `export PYTHONPATH=src` |
| `JSONDecodeError` on rules file | Validate JSON with `python -m json.tool rules/orders_rules.json` |
| All records quarantined | Check field names match sample data (`order_amount` not `amount`) |
| Regex rule never matches | Escape backslashes in JSON (`\\w` not `\w`) |
| Pass rate 0% with valid data | Ensure numeric fields are numbers in JSON, not strings |
| S3 upload `AccessDenied` | Verify IAM `s3:PutObject` on quarantine and metadata prefixes |

---

## What You Learned

- Declarative quality rules separate policy from pipeline code
- Severity levels control quarantine vs pass-with-flag behavior
- Quality reports enable SLO tracking and stakeholder communication
- The same framework pattern scales to Glue Spark and Great Expectations

---

**Next:** [Lab 4.2 – Validation Automation](../lab-4.2-validation-automation/README.md)
