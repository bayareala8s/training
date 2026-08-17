## Capstone Projects — Implementation Status

All **four** Capstone projects are implemented and runnable under `labs/week08/`.

See also: [`labs/week08/README.md`](labs/week08/README.md) · [`CAPSTONE_HANDBOOK.md`](CAPSTONE_HANDBOOK.md)

| Project | Handbook | Lab code | Status |
|---------|----------|----------|--------|
| **A — Incident Triage** | Option 1 | `labs/week08/services/incident_triage.py` | Done — API, SFN, severity, notify stub, demo |
| **B — Doc Classification** | Option 2 | `labs/week08/services/doc_classification.py` | Done — API, queues, source metadata, demo |
| **C — Approval Workflow** | Option 3 | `labs/week08/services/approval_workflow.py` | Done — request/decide, DynamoDB, SFN, demo |
| **D — Enterprise Agent** | Option 4 | `labs/week08/services/enterprise_agent.py` | Done — tools + policy + memory, demo |

### How to run one by one

```bash
cd labs
./scripts/labs.sh start && source .stack.env

./week08/option_a_incident_triage/demo.sh
./week08/option_b_doc_classification/demo.sh
./week08/option_c_approval_workflow/demo.sh
./week08/option_d_enterprise_agent/demo.sh
```

Or all: `./week08/demo_all.sh` · verify: `./scripts/verify-capstone.sh`

### Specs & grading

- `CAPSTONE_HANDBOOK.md` — options, minimum bar, rubric
- `weeks/WEEK_08.md` — Week 8 plan + quiz
- `labs/week08/README.md` — lab entry point
