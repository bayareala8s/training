# Week 8 — Capstone Labs (All 4 Projects Implemented)

Runnable implementations for **four portfolio options**. Deploy with the main course stack.

## Projects

| # | Option | Track | Endpoint | Demo |
|---|--------|-------|----------|------|
| 1 | **A** | [Incident Triage](option_a_incident_triage/README.md) | `POST /capstone/incident` | `option_a_incident_triage/demo.sh` |
| 2 | **B** | [Doc Classification](option_b_doc_classification/README.md) | `POST /capstone/document` | `option_b_doc_classification/demo.sh` |
| 3 | **C** | [Approval Workflow](option_c_approval_workflow/README.md) | `/approval/request` + `/decide` | `option_c_approval_workflow/demo.sh` |
| 4 | **D** | [Enterprise Agent](option_d_enterprise_agent/README.md) | `POST /capstone/agent` | `option_d_enterprise_agent/demo.sh` |

## Quick start

```bash
cd labs
source .venv/bin/activate
export AWS_REGION=us-east-1
export PROJECT_PREFIX=ba-la8s-ai-yourname
export BEDROCK_MODEL_ID=amazon.nova-lite-v1:0

./scripts/start.sh
source .stack.env

# Verify all four
./scripts/verify-capstone.sh

# Or run demos one by one / all
chmod +x week08/**/demo.sh week08/demo_all.sh
./week08/option_a_incident_triage/demo.sh   # 1
./week08/option_b_doc_classification/demo.sh # 2
./week08/option_c_approval_workflow/demo.sh  # 3
./week08/option_d_enterprise_agent/demo.sh   # 4
# ./week08/demo_all.sh
```

## Implementation map

| Piece | Path |
|-------|------|
| Services | `week08/services/*.py` |
| API router | `week08/lambda_capstone/handler.py` |
| SFN (A, C) | `week08/statemachine/*.asl.json` |
| Samples | `week08/samples/` |
| Unit tests | `tests/test_capstone.py` |
| Rubric | `../../CAPSTONE_HANDBOOK.md` |

## Student rule

Pick **one** option to extend for your graded portfolio. Use the other three as working references.
