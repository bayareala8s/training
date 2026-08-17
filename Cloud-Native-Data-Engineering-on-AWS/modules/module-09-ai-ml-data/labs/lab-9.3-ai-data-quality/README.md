# Lab 9.3: AI Data Quality Validation

> 📊 **Diagrams:** [Mermaid](diagram.md) · [Draw.io (lab-9.3-ai-data-quality.drawio)](../../../../docs/diagrams/drawio/lab-9.3-ai-data-quality.drawio) · [PNG](../../../../docs/diagrams/png/lab-9.3-ai-data-quality.png) · [SVG](../../../../docs/diagrams/svg/lab-9.3-ai-data-quality.svg)

**Estimated time:** 90 minutes · **Module 9**

---

## Objectives

- Apply ML-specific quality checks beyond traditional validation (Module 4)
- Detect label imbalance, feature drift (PSI), and potential leakage
- Validate training datasets before SageMaker or downstream model training
- Generate an AI quality report suitable for ML team sign-off
- Integrate quality gates into the ML data pipeline

---

## Prerequisites

- Lab 9.1 complete (`output/train.parquet`, `output/test.parquet` exist)
- Python 3.10+ with `pandas`, `pyarrow`

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
train.parquet + test.parquet (Lab 9.1)
        │
        ▼
ai_quality_rules.json
        │
        ▼
ai_quality_validator.py
        │
        ├── Label balance check
        ├── Null rate check
        ├── PSI drift (train vs test)
        ├── Leakage correlation audit
        ├── Duplicate entity check
        └── Feature range validation
        │
        ▼
output/ai_quality_report.json
```

---

## Project Structure

```text
lab-9.3-ai-data-quality/
├── README.md
├── src/
│   ├── ai_quality_rules.json
│   └── ai_quality_validator.py
└── output/
    └── ai_quality_report.json
```

---

## Step 1: Review AI Quality Rules

Open `src/ai_quality_rules.json`. Compare to Module 4 rules:

| Check | Module 4 Equivalent | AI-Specific Aspect |
|-------|---------------------|-------------------|
| Label balance | — | Class imbalance breaks many classifiers |
| Feature null rate | Completeness | Imputation strategy depends on rate |
| PSI drift | — | Train/test distribution shift |
| Leakage correlation | — | Future info in features |
| Duplicate entities | Uniqueness | Same customer twice per snapshot |
| Feature range | Range rules | Sanity bounds for engineered features |

---

## Step 2: Run Validator

Ensure Lab 9.1 output exists:

```bash
cd modules/module-09-ai-ml-data/labs/lab-9.1-ml-dataset-prep
python3 src/prepare_ml_dataset.py --snapshots 12

cd ../lab-9.3-ai-data-quality
python3 src/ai_quality_validator.py
```

Review console output and report:

```bash
python3 -m json.tool output/ai_quality_report.json
```

Expected structure:

```json
{
  "overall_passed": true,
  "error_count": 0,
  "warning_count": 0,
  "checks": [ ... ]
}
```

---

## Step 3: Inject a Leakage Failure (Learning Exercise)

Create a leaky feature to test detection:

```bash
python3 << 'EOF'
import pandas as pd
from pathlib import Path

for split in ["train", "test"]:
    p = Path("../lab-9.1-ml-dataset-prep/output") / f"{split}.parquet"
    df = pd.read_parquet(p)
    df["leaky_future_spend"] = df["total_spend_30d"] * df["will_purchase_again_30d"] * 10
    df.to_parquet(p, index=False)
print("Injected leaky_future_spend column.")
EOF

python3 src/ai_quality_validator.py || true
```

The **leakage_correlation** check should fail. Document the finding, then restore data:

```bash
cd ../lab-9.1-ml-dataset-prep && python3 src/prepare_ml_dataset.py --snapshots 12
cd ../lab-9.3-ai-data-quality && python3 src/ai_quality_validator.py
```

---

## Step 4: Add Custom Check

Extend `ai_quality_rules.json` with a **minimum row count** check for the test split. Implement in `ai_quality_validator.py` or document as a Step Functions gate:

```json
"min_test_rows": {
  "split": "test",
  "min_rows": 50,
  "severity": "error"
}
```

Document your implementation in `LAB-REPORT.md`.

---

## Step 5: Pipeline Quality Gate

Design where this validator runs in the end-to-end flow:

```text
Curated ETL → Feature Pipeline (Lab 9.2) → ML Dataset Prep (Lab 9.1)
                                                    │
                                                    ▼
                                          AI Quality Validator
                                                    │
                              Pass ──→ Upload to ml/training/
                              Fail ──→ Quarantine + SNS alert
```

Create `quality-gate-design.md`:

```markdown
# ML Data Quality Gate

## Trigger
After `prepare_ml_dataset.py` completes successfully.

## Pass Criteria
- overall_passed = true in ai_quality_report.json
- zero error-severity checks

## Fail Actions
1. Do NOT promote dataset to ml/training/production/
2. Write report to s3://bucket/quarantine/ml/<run_id>/
3. Publish CloudWatch metric: MLQualityGateFailed
4. SNS notify ML + data engineering

## Sign-off
ML team reviews report before SageMaker training job starts.
```

---

## Step 6: Upload Report to S3

```bash
export BUCKET=$(cd ../../../../infrastructure/environments/dev && terraform output -raw data_lake_bucket)

aws s3 cp output/ai_quality_report.json \
  s3://$BUCKET/metadata/ml-quality-reports/customer-churn/$(date -u +%Y-%m-%d)_report.json
```

---

## Step 7: Lab Report

Create `LAB-REPORT.md`:

```markdown
# Lab 9.3 Report

## Validation Result
Overall passed: Yes/No

## Checks Summary
| Check | Result | Notes |
|-------|--------|-------|

## Leakage Exercise
What happened when leaky_future_spend was added?

## Quality Gate Design
Link to quality-gate-design.md

## Production Recommendations
What would you add for a recommendation system dataset?
```

---

## Deliverables

- [ ] `ai_quality_report.json` generated with drift, leakage, and balance checks
- [ ] Quality gate pass/fail documented for train/val/test splits
- [ ] `LAB-REPORT.md` with checks summary and production recommendations

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `FileNotFoundError: train.parquet` | Run Lab 9.1 first |
| PSI warnings on small samples | Expected with synthetic data; note in report |
| All checks pass with leaky column | Lower `max_abs_correlation` or check column dtype |

---

## What You Learned

- ML-specific quality dimensions (drift, leakage, label balance)
- Automated quality gates before model training
- Extending Module 4 validation patterns for AI workloads
- Quality reports as ML team sign-off artifacts

**Next:** [Assignment 9 – AI Recommendation Pipeline Design](../../assignments/assignment-09.md)
