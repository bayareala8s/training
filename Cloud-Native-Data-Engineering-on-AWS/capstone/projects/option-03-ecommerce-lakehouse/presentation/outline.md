# Presentation Outline – Option 3 E-Commerce Analytics Lakehouse

**Duration:** 15–20 minutes + Q&A  
**Project:** `cnde-cap-ecommerce`

---

## Slide Deck (14 slides)

| # | Slide | Time | Talking points |
|---|-------|------|----------------|
| 1 | Title | 0:30 | E-Commerce Analytics Lakehouse · Option 3 · course name · date |
| 2 | Business problem | 1:30 | Spreadsheet reconciliation; bad amounts in dashboards; Athena cost on raw CSV |
| 3 | Requirements | 1:00 | Batch + clickstream; star schema; quality ≥85%; cost-efficient Athena |
| 4 | Architecture overview | 2:00 | Mermaid/context diagram: OMS/PIM/CRM/Web → medallion → Athena |
| 5 | Data zones | 1:00 | raw / cleaned / curated / quarantine / metadata paths |
| 6 | Star schema | 1:30 | fact_orders grain + dim_products + dim_customers + clickstream facts |
| 7 | Ingestion patterns | 1:00 | Nightly CSV batch vs JSON clickstream micro-batches |
| 8 | Data quality | 1:30 | Rules (≥5/dataset); quarantine demo; pass-rate report |
| 9 | Governance | 1:00 | Email masking; role matrix; tags `Project=capstone-option-3` |
| 10 | Cost | 1:00 | ~$15/mo pilot model; partition pruning; lab-cycle stop |
| 11 | Demo | 3:00 | Local pipeline + quarantine + curated fact sample |
| 12 | Lessons learned | 1:00 | Star schema first; warnings ≠ quarantine; Parquet for Athena |
| 13 | Roadmap | 0:30 | Streaming clickstream; SCD2 dims; Lake Formation |
| 14 | Q&A / repo | — | Repo path, how to re-run `scripts/run_local.sh` |

---

## Demo Script (~5 minutes)

### Prep

- [ ] `cd option-03-ecommerce-lakehouse && bash scripts/run_local.sh`
- [ ] Open `output/metadata/quality-reports/`
- [ ] Open `output/quarantine/orders/.../failed.json`
- [ ] Open `output/curated/orders/.../data.csv` (fact_orders)

### Flow

| Step | Action | Say |
|------|--------|-----|
| 1 | Show `sample-data/orders.csv` bad rows | "We planted negative amounts and invalid statuses on purpose." |
| 2 | Run or show pipeline console output | "Shared runner validates with Lab 4.1 rules, then curates." |
| 3 | Open quarantine JSON | "Failures never reach fact_orders—stewards see `_violations`." |
| 4 | Show curated fact columns | "Grain is order_id, customer_id, product_id, amount, status, date." |
| 5 | Show dim_customers masked email | "PII is masked before analytics." |
| 6 | (Optional) Athena screenshot | "Analysts query Parquet partitions—not raw CSV." |

### Fallback

If live run fails, use committed screenshots of `output/` from a prior successful run and narrate the same story.
