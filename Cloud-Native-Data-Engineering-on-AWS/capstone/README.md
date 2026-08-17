# Capstone Projects — All 4 Options (Reference Implementations)

Each option is a **complete, runnable** capstone project: sample data, validation rules, curated ETL, docs, diagrams, and presentation outline.

| Option | Path | Industry focus | Project key |
|--------|------|----------------|-------------|
| **1** | [option-01-banking-regulatory](projects/option-01-banking-regulatory/) | Regulatory settlement reporting | `cnde-cap-banking` |
| **2** | [option-02-healthcare-analytics](projects/option-02-healthcare-analytics/) | Patient analytics + PII masking | `cnde-cap-healthcare` |
| **3** | [option-03-ecommerce-lakehouse](projects/option-03-ecommerce-lakehouse/) | Sales lakehouse + star schema | `cnde-cap-ecommerce` |
| **4** | [option-04-enterprise-platform](projects/option-04-enterprise-platform/) | Full platform (Modules 1–9) | `cnde-cap-enterprise` |

Shared runner: [projects/_shared/run_pipeline.py](projects/_shared/run_pipeline.py)

---

## What is the Capstone?

Week 10 final project (30% of grade). Students normally pick **one** option and customize it. These folders are **reference implementations** you can demo, teach from, or fork into `capstone/my-project`.

---

## Run any option locally (no AWS)

```bash
cd capstone/projects/option-01-banking-regulatory
bash scripts/run_local.sh
# Inspect output/raw, cleaned, curated, quarantine, metadata
```

Same pattern for options 02–04.

---

## Optional: upload to AWS

```bash
# From course root
./scripts/lab-cycle.sh start
source ./scripts/lab-env.sh   # use bash

cd capstone/projects/option-03-ecommerce-lakehouse
python3 ../_shared/run_pipeline.py --project-root . --upload --bucket "$BUCKET"
```

Tear down when done: `./scripts/lab-cycle.sh stop --yes`

---

## Per-option contents

Every project includes:

- `README.md` — overview + run instructions  
- `pipeline.json` — datasets wiring  
- `sample-data/` — synthetic data (includes bad records)  
- `src/validation/rules/` — Lab 4.1-style rules  
- `src/etl/` — curated transforms + Glue job  
- `docs/` — ARCHITECTURE, GOVERNANCE, COST-ANALYSIS  
- `architecture/diagrams/` — Mermaid  
- `presentation/outline.md` — slide + demo script  
- `infrastructure/README.md` — AWS tagging / lab-cycle notes  

---

## Student workflow (graded submission)

1. Pick **one** option (or start from the blank template)  
2. Copy to your working folder:

```bash
cp -r capstone/projects/option-03-ecommerce-lakehouse capstone/my-project
# OR blank template:
cp -r capstone/templates/project-structure capstone/my-project
```

3. Customize for your name, scenario tweaks, and AWS tags  
4. Follow [modules/module-10-capstone/assignments/capstone-checklist.md](../modules/module-10-capstone/assignments/capstone-checklist.md)  
5. Present using [presentation-guide.md](presentation-guide.md)  
6. Graded with [rubric.md](rubric.md)

---

## Related

- [Module 10 README](../modules/module-10-capstone/README.md)  
- [Week 10 Lecture](../modules/module-10-capstone/lectures/week-10-lecture.md)  
- Blank template: [templates/project-structure](templates/project-structure/)
